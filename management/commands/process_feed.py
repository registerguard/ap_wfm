#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
TO DO:

* Make insertion date sensitive, so lottery, top stories don't bork, things
with slugs that don't change, don't mess up the URL. Add date to URL in these
cases?

* Also, check published date/time: If it's in the future, don't insert!

* from django.template.defaultfilters import slugify

* Check both slugify(title) and 'headline'; if either match, you've got a
replacement

* Deal with FastStory's from the AP (sometimes they can be good ... )

'''

import datetime
import logging
import logging.handlers
import os
import re
import sys
import time
import urllib2
from ap_wfm.models import APStory, Image, Category
from ap_wfm_settings import FROM_EMAIL, RECIPIENT_LIST, WIRE_CATEGORY_DICT, \
    WIRE_PROCESSING

from dateutil.parser import parse as dateParser
from django.core.exceptions import MultipleObjectsReturned
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from django.core.mail import send_mail
from django.core.management.base import BaseCommand, CommandError
from django.db import IntegrityError
from django.db.utils import DatabaseError
from django.template.defaultfilters import slugify, date
from lxml import objectify, etree

'''
If parsing the Arts, and you get this:

If e['{http://ap.org/schemas/03/2005/apcm}ContentMetadata'].Source.text == 'McClatchy/Tribune - MCT Information Services'

... then skip!
'''

def skip_entry_test(title_text, list_of_frags_to_skip, the_log):
    for title_frag in list_of_frags_to_skip:
        if title_frag and title_frag in title_text:
            the_log.debug('   *** NEW SKIPPER: Skipped %s entry. Skipped because disallowed fragment \'%s\' was in \'%s\'. ***' % (title_text, title_frag, title_text))
            return True
        else:
            continue
    # if we got this far, must all be good titles, so don't skip, i.e., return False!
    return False

class Command(BaseCommand):
    args = 'The full path to the AP XML file.'
    help = 'Parses, imports AP WebFeeds XML into Django databoase.'

    # clear out any previous category
    category = None

    def handle(self, *args, **options):
        log_file_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)))
        ap_content_feed = args[0].split(os.path.sep)[-2]

        logger = logging.getLogger(__name__)
        logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)-6s: %(name)s - %(levelname)s - %(message)s')
        handler = logging.StreamHandler()
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        fileLogger = logging.handlers.RotatingFileHandler(filename=( log_file_dir + '/%s_xml_into_Django.log' % ap_content_feed ), maxBytes=256*1024, backupCount=5) # 256 x 1024 = 256K
        fileLogger.setFormatter(formatter)
        logger.addHandler(fileLogger)

        logger.debug('>>> Script called.')
        start_time = time.time()

        try:
            logger.debug('%s passed to script.' % args[0])
        except IndexError, err:
            logger.error('You need to supply a path to a xml file.')
            return

        if args[0].count('/feeds/'):
            # ['', 'rgcalendar', 'oper', 'WFA', 'RemoteHeadlines', 'feeds', 'Oregon-JH', 'feed_2013-02-07T04-13-11.408Z.xml']
            directory_xml_file = tuple(args[0].split(os.path.sep)[-2:])
            logger.debug( '>>> STARTING /%s/%s' % directory_xml_file )

            try:
                doc = objectify.parse(args[0])
                tree = doc.getroot()
            except IOError, err:
                logger.error(err)
                message = u'''Problem inserting AP web feeds story(ies).

The following error happened:
%s.

Typically the problem is the permissions on the /tmp/cbs3cache/
directory have been set to owner-only write and this seems to
happen everytime go.registerguard.com gets restarted.
The solution is to open up the write permissions on
/tmp/cbs3cache/, then these emails should cease.''' % err
                send_mail(
                    u'[Django] Problem with ap_wfm import script (/rgcalendar/oper/WFA/processFeed.py)',
                    message,
                    FROM_EMAIL,
                    RECIPIENT_LIST,
                    fail_silently=False
                )
                return

            # Figure out which section this feed is going to go into.
            # Each section requires entry into WIRE_CATEGORY_DICT above.
            for t in tree.title:
                section_lookup_key = t['{http://www.w3.org/1999/xhtml}div'].span.text
                category = WIRE_CATEGORY_DICT[section_lookup_key]
                logger.debug('>>> Feeding \'%s\' section.' % category)

            # ugly, ugly hack to prevent race condition
            start_delay = WIRE_PROCESSING[ap_content_feed]['delay']
            time.sleep(start_delay)
            print 'start_delay:', start_delay

            skip_title_fragments = WIRE_PROCESSING[ap_content_feed]['skip_title']
            if skip_title_fragments:
                logger.debug('>>> Skip Title fragments: %s' % str(skip_title_fragments))

            for e in tree.entry:
                logger.debug(' ')
                logger.debug('============')
                logger.debug('    %s' % e.title.text)

                if 'New York Times' in e.rights.text:
                    logger.debug('    Skipping %s as it is NYTimes content.' % e.title.text)
                    continue

                if skip_entry_test(e.title.text, skip_title_fragments, logger):
                    continue

                # using slugline to weed out NYT, MCT stories from arts, tech and dc feeds
                if ap_content_feed in ('Arts-Entertainment-JH', 'Technology-JH', 'Washington-DC-JH'):
                    if skip_entry_test(e['{http://ap.org/schemas/03/2005/apcm}ContentMetadata'].SlugLine.text, skip_title_fragments, logger):
                        continue

                # using headline to weed out agate box from washington state feed
                if ap_content_feed in ('Washington-State-JH'):
                    if skip_entry_test(e.content['{}nitf'].body['body.head'].hedline.hl1.text, skip_title_fragments, logger):
                        continue

                # using contributor to weed out content from 'The Register-Guard'
                if ap_content_feed in ('Oregon-JH'):
                    # See if there's a "contributor" element and if it says "The Register-Guard"
                    try:
                        if skip_entry_test(e.contributor.name.text, skip_title_fragments, logger):
                            continue
                    except AttributeError, err:
                        logger.debug('>>> No "contributor" element: %s' % err)

                # See if 'FullStory' is in <apcm:ContentElement>
                try:
                    content_element = getattr(e['{http://ap.org/schemas/03/2005/apcm}ContentMetadata'].ContentElement, "text", '')
                except AttributeError:
                    content_element = ''

                # Patching in AP FastStory's ...

                # if content_element == 'FullStory':
                if content_element == 'FullStory' or content_element == 'FastStory':
                    full_story = True
                    fast_story = False
                elif content_element == 'FastStory':
                    fast_story = True
                    full_story = False
                else:
                    full_story = False
                    fast_story = False

                # See if story is AP staff written
                try:
                    the_source = getattr(e['{http://ap.org/schemas/03/2005/apcm}ContentMetadata'].Source, "text", '')
                    if the_source == 'AP':
                        ap_staff_written = True
                    else:
                        ap_staff_written = False

                    if the_source == 'New York Times Syndicate':
                        nyt = True
                    else:
                        nyt = False

                    print 'The SOURCE:', the_source
                except:
                    pass

                # If it's a NYT TIMES EXPRESS article, then skip it.
                # e['{http://ap.org/schemas/03/2005/apcm}ContentMetadata'].SubjectClassification.attrib['Value']
                try:
                    nyt_te = getattr(e['{http://ap.org/schemas/03/2005/apnm}NewsManagement'].PublishingSpecialInstructions, "text", '')
                except AttributeError:
                    nyt_te = ''
                if nyt_te.count('article is part of TIMES EXPRESS'):
                    logger.debug( '   Note: %s is a New York Times Express article and thus will not be saved.' % e.title.text )
                    continue

                # If it's an AP staff written story, but isn't FullStory (or FastStory), then skip it.
                if ap_staff_written and not full_story:
                    logger.debug( '   Note: This AP story, %s, is not a \'FullStory\', so will not be saved.' % e.title.text )
                    continue

                try:
                    headline = getattr(e['{http://ap.org/schemas/03/2005/apcm}ContentMetadata'].HeadLine, "text", '')
                except AttributeError:
                    headline = ''

                if not headline:
                    headline = getattr(e.content['{}nitf'].body['body.head'].hedline.hl1, "text", '')

                # Get a count of the <block id="Main"> in the current story
                block_count = len( e.content['{}nitf'].body['body.content'].findall('block') )

#                 # If multiple <block id="Main">s on Oregon wire, then it's a Lottery round-up
#                 if block_count > 1 and ap_content_feed in ('Oregon-JH') and \
#                     e['{http://ap.org/schemas/03/2005/apcm}ContentMetadata'].SubjectClassification.attrib['Value'] == 'j':

                # Re the above: "<block id="Main">s on Oregon wire, then it's a Lottery round-up"
                # Not sure why I wouldn't want all <blocks> that are within a <block id ="Main">
                # to get concatenated? Why was I checking for Oregon/j-wire? Whelp, I'm going to
                # take those two checks out and see what happens ...
                if block_count > 1:
                    body_text = ''
                    main_blocks = e.content['{}nitf'].body['body.content'].iterfind('block')
                    for main_block in main_blocks:
                        print '.getchildren():', main_block.getchildren()

                        # Finds all <hl2> and <p> blocks of text
                        print '.findall(\'hl2|p\'):', main_block.findall('hl2|p')

                        main_blocks_list = []
                        for main_block_child in main_block.iterchildren():
                            main_blocks_list.append(etree.tostring( main_block_child, pretty_print=True ))
                        body_text += ''.join(main_blocks_list)

                    body_text = body_text.replace(
                        ' xmlns="" xmlns:apcm="http://ap.org/schemas/03/2005/apcm" xmlns:apnm="http://ap.org/schemas/03/2005/apnm" xmlns:georss="http://www.georss.org/georss" xmlns:o="http://w3.org/ns/odrl/2/"',
                        ''
                    )
                    body_text = body_text.replace('<p/>', '')
                    body_text = body_text.replace('hl2', 'h2')

                    if headline.count('OR Lott'):
                        headline = headline.replace('OR Lottery', 'Oregon Lottery')

                    if headline.count('CA Lott'):
                        headline = headline.replace('CA Lottery', 'California Lottery')
                elif block_count == 1:
                    # multiple <block> trees, need to find <block id="Main">
                    if e.content['{}nitf'].body['body.content'].block.attrib['id'] == 'Main':
                        body_text = etree.tostring( e.content['{}nitf'].body['body.content'].block, pretty_print=True)

                    # If body.content.block has 'Caption' attrib, it's a photo!
                    elif e.content['{}nitf'].body['body.content'].block.attrib['id'] == 'Caption':
                        body_text = etree.tostring( e.content['{}nitf'].body['body.content'].block, pretty_print=True)

                # Treat the text here
                body_text = body_text.replace('(AP) ', '')

                try:
                    location = e.content['{}nitf'].body['body.head'].dateline.location.text
                except AttributeError:
                    location = ''

                try:
                    e.contributor
                    contributor = e.contributor.name.text
                    contributor_uri = e.contributor.uri.text
                except AttributeError:
                    contributor = ''
                    contributor_uri = ''

                try:
                    byline = getattr(e['{http://ap.org/schemas/03/2005/apcm}ContentMetadata'].ByLine, "text", '')
                except AttributeError:
                    byline = ''
                print 'BYLINE:', byline

                try:
                    byline_title = e['{http://ap.org/schemas/03/2005/apcm}ContentMetadata'].ByLine.attrib['Title']
                except (AttributeError, KeyError), err:
                    byline_title = ''
                print 'BYLINE_TITLE:', byline_title

                try:
                    # extracted management_id looks like this: 'urn:publicid:ap.org:8e4e23b249ca4eaa92806a0250166a06'
                    management_id = getattr(e['{http://ap.org/schemas/03/2005/apnm}NewsManagement'].ManagementId, "text", '').split(':')[-1]
                except AttributeError:
                    management_id = ''

                if e['{http://ap.org/schemas/03/2005/apcm}ContentMetadata'].ConsumerReady.text == 'FALSE':
                    consumer_ready = False
                else:
                    consumer_ready = True

                try:
                    keywords = e['{http://ap.org/schemas/03/2005/apcm}ContentMetadata'].Keywords.text
                except AttributeError:
                    keywords = headline

                try:
                    ap_subject_code = e['{http://ap.org/schemas/03/2005/apcm}ContentMetadata'].SubjectClassification.attrib['Value']
                except AttributeError:
                    ap_subject_code = ''

                # A one-off to change 'BC-OR--Portland Stocks, OR' into 'Portland Stocks'
                if ap_subject_code == 'f' and (ap_content_feed == 'Oregon-JH') and headline.count('-'):
                    headline = keywords
                    body_text = body_text.replace('&lt;</td>', '</td>')
                    body_text = body_text.replace(';', '</td><td>')
                    body_text = body_text.replace('<td>Name Ticker High Low Last Change Change Ratio</td>', '<th>Name</th><th>Ticker</th><th>High</th><th>Low</th><th>Last</th><th>Change</th><th>Change Ratio</th>')

                    time_stamp_string = re.search(r'\d{12}', body_text)
                    if time_stamp_string:
                        stock_info_datetime = datetime.datetime.strptime(time_stamp_string.group(0), '%Y%m%d%H%M')
                        # Adjust time from Eastern time zone.
                        stock_info_datetime = stock_info_datetime - datetime.timedelta(hours=3)
    #                   pretty_stock_info_datetime = stock_info_datetime.strftime('%A, %B %d, %Y, %I:%M %p')
                        pretty_stock_info_datetime = date(stock_info_datetime, 'P, N j, Y')
                        body_text = body_text.replace(time_stamp_string.group(0), pretty_stock_info_datetime)
                APStory_instance = APStory(
    #                 category = ap_cat,
                    updated = dateParser(e.updated.text),
                    published = dateParser(e.published.text),
                    management_id = management_id,
                    consumer_ready = consumer_ready,
                    media_type = e['{http://ap.org/schemas/03/2005/apcm}ContentMetadata'].MediaType.text,
                    priority_numeric = e['{http://ap.org/schemas/03/2005/apcm}ContentMetadata'].Priority.attrib['Numeric'],
                    priority_legacy = e['{http://ap.org/schemas/03/2005/apcm}ContentMetadata'].Priority.attrib['Legacy'],
                    subject_code = ap_subject_code,
                    location = location,
                    contributor = contributor,
                    contributor_uri = contributor_uri,
                    byline = byline,
                    byline_title = byline_title,
                    slugline = e['{http://ap.org/schemas/03/2005/apcm}ContentMetadata'].SlugLine.text,
                    title = e.title.text,
                    keywords = keywords,
                    headline = headline,
    #                 slug = slugify(headline),
                    slug = slugify(e.title.text),
                    body = body_text,
                )

                ap_cat, created = Category.objects.get_or_create(name=category)

                try:
                    # Gather up any multiple versions that may have creeped in ...
    #                 old_version_qs = APStory.objects.filter(headline=headline).order_by('-id')
    #                 old_version_qs = APStory.objects.filter(slug=slugify(headline)).order_by('-id')
    #                 old_version_qs = APStory.objects.filter(keywords=keywords).order_by('-id')
    #                 old_version_qs = APStory.objects.filter(management_id=management_id, category=ap_cat).order_by('-id')
    #                 old_version_qs = APStory.objects.filter(title=e.title.text, category=ap_cat).order_by('-id')
    #                 old_version_qs = APStory.objects.filter(slug=slugify(e.title.text), category=ap_cat).order_by('-id') - 5/6/2013
                    '''
                    When looking up by management_id, be sure to also include the
                    category in the lookup, otherwise you'll only get one instance
                    of a story posted in multiple categories.

                    Reminder: Pipe ("|") returns a union of QuerySets: All items
                    from qs1 and qs2, removing dupes.
                    '''

                    old_cats = []

    #                 old_version_qs = APStory.objects.filter( slug=slugify(e.title.text), category=ap_cat ) | APStory.objects.filter( management_id=management_id, category=ap_cat ).order_by('-id')
    #                 old_version_qs = APStory.objects.filter( slug=slugify(e.title.text), category=ap_cat ) | APStory.objects.filter( management_id=management_id, category=ap_cat ).order_by('-id')
                    old_version_qs = ( APStory.objects.filter( slug=slugify(e.title.text) ) | APStory.objects.filter( management_id=management_id ) ).order_by('-id')
                    # old_version_qs = APStory.objects.filter( management_id=management_id ).order_by('-id')
                    logger.debug( 'XXX Older version look-up based on slug: \'%s\', management_id: %s XXX' % (slugify(e.title.text), management_id) )
                    if old_version_qs:
                        if len(old_version_qs) > 1:
                            logger.debug( 'MULTIPLE STORIES FOUND: %s' % old_version_qs )
                        logger.debug( 'XXX Found older version: %s XXX' % old_version_qs )
                        # iterate over each APStory in QuerySet to find which
                        # Categories older version belonged to.
                        for old_story in old_version_qs:
                            old_story.created = datetime.datetime.now()
                            old_story.updated = dateParser(e.updated.text)
                            old_story.published = dateParser(e.published.text)
                            old_story.management_id = management_id
                            old_story.consumer_ready = consumer_ready
                            old_story.media_type = e['{http://ap.org/schemas/03/2005/apcm}ContentMetadata'].MediaType.text
                            old_story.priority_numeric = e['{http://ap.org/schemas/03/2005/apcm}ContentMetadata'].Priority.attrib['Numeric']
                            old_story.priority_legacy = e['{http://ap.org/schemas/03/2005/apcm}ContentMetadata'].Priority.attrib['Legacy']
                            old_story.subject_code = ap_subject_code
                            old_story.location = location
                            old_story.contributor = contributor
                            old_story.contributor_uri = contributor_uri
                            old_story.byline = byline
                            old_story.byline_title = byline_title
                            old_story.slugline = e['{http://ap.org/schemas/03/2005/apcm}ContentMetadata'].SlugLine.text
                            old_story.title = e.title.text
                            old_story.keywords = keywords
                            old_story.headline = headline
                            old_story.slug = slugify(e.title.text)
                            old_story.body = body_text
                            old_story.save()
                            APStory_instance = old_story
                            logger.debug('XXX UPDATED %s XXX' % e.title.text)
                            # iterate over categories in each story
                            for old_cat in old_story.category.all():
                                old_cats.append(old_cat)
                        logger.debug( '    RETRIEVED CATEGORY/IES: %s' % old_cats )
                        if old_version_qs[:1]:
                            old_version_qs_list = old_version_qs[1:]
                            for old_version in old_version_qs_list:
                                old_version.delete()
                                logger.debug( '    DELETED %s!' % old_version )
                    else:
                        # Save the newest one ...
                        APStory_instance.save()
                        logger.debug('XXX CREATED {0} XXX'.format(e.title.text))

                    if old_cats:
                        for salvaged_cat in old_cats:
                            logger.debug( '        ADDING RETRIEVED CATEGORY: %s to %s' % (salvaged_cat, APStory_instance.headline) )
                            salvaged_cat_id, cat_created = Category.objects.get_or_create(name=salvaged_cat.name)
                            APStory_instance.category.add(salvaged_cat_id)
                    if ap_cat not in APStory_instance.category.all():
                        print '        ADDING NEW CATEGORY'
                        APStory_instance.category.add(ap_cat)
                except (IntegrityError, DatabaseError), err:
                    print 'The error:', err
                    print 'Problem saving "%s" to database.' % APStory_instance.title

                # Photos attached to stories ...
                media_items = e.content['{}nitf'].body['body.content'].iterfind('media')
                media_count = len(e.content['{}nitf'].body['body.content'].findall('media'))
                logger.debug('      %s images with this story.' % media_count)

                # This regex for caption "OUT" clean-up below.
                # A test/experimental script: ~/Scripts/Python/regex_trim_from_end.py
                # Also, https://regex101.com/#python with the "g" modifier
                regex = re.compile(r"(\b[A-Z, /:;.-]+\b\.?)$")

                if media_items:

                    for media_item in media_items:
                        caption = media_item['media-caption'].p.text.strip()

                        '''
                        strip out stuff such as TV OUT; MAGS OUT; MANDATORY CREDIT;
                        BATAVIA DAILY NEWS OUT; DUNKIRK OBSERVER OUT; JAMESTOWN
                        POST-JOURNAL OUT; LOCKPORT UNION-SUN JOURNAL OUT; NIAGARA
                        GAZETTE OUT; OLEAN TIMES-HERALD OUT; SALAMANCA PRESS OUT;
                        TONAWANDA NEWS OUT
                        from the end of captions
                        '''
                        r = regex.search(caption)
                        if r:
                            caption = caption.replace(r.groups()[0], '').rstrip()

                        # "AP Photo" is 'name' of biggest image
                        if media_item['media-reference'][0].attrib['name'] == "AP Photo":
            #                 # "AP Preview Image" is name of middle-sized image
            #                 if media_item['media-reference'][1].attrib['name'] == "AP Preview Image":
                            print '    Media ref.:', media_item['media-reference'].attrib['source']
                            photo_url = media_item['media-reference'].attrib['source']
                            media_name_hash = media_item['media-reference'].attrib['id'].split(':')[1]
                            try:
                                alt_text = media_item['media-reference'][1].attrib['alternate-text']
                                # For use by non-AP staff, Oregon Marketplace/Region images below
                                orig_file_name = alt_text
                                ap_ext = 'jpg'
                            except KeyError, err:
                                logger.debug('      No alternate-text in a photo associated with %s' % e.title.text)
                                alt_text = 'AP image'
                            try:
                                media_source = media_item['media-producer'][0].text.strip()
            #                     media_source = media_item['media-producer'][1].text.strip()
                            except AttributeError:
                                media_source = ''

                            # munge through the many media-metadata elements that
                            # accompany each image to find the first reference
                            # to OriginalFileName (only found in staff AP images/
                            # non-Oregon Marketplace/Region images) ...
                            media_metas = media_item.iterfind('media-metadata')
                            for media_meta in media_metas:
                                if media_meta.attrib['name'] == 'OriginalFileName':
                                    # AP includes extension in OriginalFileName
                                    # 'value'. Need to split apart.
                                    (orig_file_name, ap_ext) = media_meta.attrib['value'].split('.')
                                    break

                            orig_file_name = '%s-%s.%s' % (orig_file_name, media_name_hash, ap_ext)

                            try:
                                img_temp = NamedTemporaryFile(delete=True)
                                img_temp.write(urllib2.urlopen(photo_url).read())
                                img_temp.flush()

                                im = Image(
                                    apstory = APStory_instance,
                                    caption = caption,
                                    alt_text = alt_text,
                                    original_filename = orig_file_name,
                                    source = media_source,
                                )

                                try:
                                    try:
                                        # I think this lookup could be a trouble
                                        # spot as there could be an Image in DB
                                        # with an orig_file_name of ''
                                        img = Image.objects.get(original_filename = orig_file_name)
                                    except MultipleObjectsReturned, err:
                                        logger.debug('      Tried %s; but there was an error: %s' % (img.original_filename, err))
                                        pass
                                    '''
                                    Just because image is in database, doesn't mean it's
                                    associated with this particular APStory instance ...
                                    '''
                                    if img:
                                        APStory_instance.image_set.add(img)
                                except Image.DoesNotExist:
                                    logger.debug('      Didn\'t find image %s; downloading ... ' % orig_file_name)
                                    im.image.save(orig_file_name, File(img_temp))

                            except urllib2.HTTPError:
                                logger.debug('IMAGE NOT IMPORTING. You may not have the AP Web Feeds manager running. It needs to be.')
                                continue

    #                         im.image.save(file_name, File(img_temp))

    #             old_version_qs = APStory.objects.filter(title=APStory_instance.title).order_by('-id')
    #             if old_version_qs.count() > 1:
    #                 for old_version in old_version_qs[1:]:
    #                     logger.debug('      *** %s, Id %s deleted' % (old_version.title, old_version.id))
    #                     old_version.delete()

        else:
            logger.debug('Item %s ignored.' % (args[0]))

        elapsed_time = time.time() - start_time
        logger.debug( '>>> FINISHED /%s/%s.' % directory_xml_file )
        logger.debug( '>>> Took %s to run ... \n' % ( str(datetime.timedelta(seconds=elapsed_time))) )
