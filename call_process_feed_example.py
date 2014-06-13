#!/usr/bin/env python
def main():
    import os, sys
    from os import environ
    '''
    The first sys.path.append adds the parent directory of call_process_feed.py 
    to sys.path.
    The second sys.path.append bit adds the path to your Django project 
    settings.
    These two sys.path.append examples assume your Django project directory 
    is next to your ap_wfm directory. Like this:
    
    ├── ap_wfm
    │   ├── README.md
    │   ├── WFA
    │   │   ├── config
    │   │   │   └── configuration.xml
    │   │   ├── feeds
    │   │   │   ├── OneOfYourFeeds
    │   │   │   │   ├── feed_646541_2014-06-12T00-51-22.558Z.xml
    │   │   │   │   ├── feed_646541_2014-06-12T01-12-34.622Z.xml
    │   │   │   │   ├── feed_646541_2014-06-12T01-33-38.907Z.xml
    │   │   │   │   ├── feed_646541_2014-06-12T23-08-39.370Z.xml
    │   │   │   │   ├── feed_646541_2014-06-12T23-14-02.723Z.xml
    
        [ ... ]
    
    │   │   └── logs
    │   │       ├── WebFeedsAgent.log
    │   │       └── WebFeedsAgent.log.2014-06-11.1
    ├── your_project_dir
    │   ├── README.rst
    │   ├── __init__.py
    │   ├── ap_wfm -> ../ap_wfm    
    
    Your may need to adjust the number of relative path moves '..' to suit 
    your particular layout.
    
    '''
    sys.path.append(os.path.join(os.path.abspath(os.path.dirname(__file__)),
                             '..'))
    sys.path.append(os.path.join(os.path.abspath(os.path.dirname(__file__)),
                             '../your_project_dir'))
    environ['DJANGO_SETTINGS_MODULE'] = 'your_project_dir.settings'
    
    if len(sys.argv) > 1:
        path_to_xml = sys.argv[1]
        
        from django.core import management
        management.call_command('process_feed', path_to_xml)
    else:
        raise ValueError('Need to supply a path to XML file.')

if __name__ == "__main__": main()
