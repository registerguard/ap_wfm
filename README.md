ap_wfm
======

AP WebFeeds Manager parser

[Install requirements](#install-requirements)

Install requirements
--------------------

1. An [AP Exchange](http://www.apexchange.com/) Saved Search news feed. At least one, but several can work at the same time. We've got ~16 going at a time.
1. An [AP WebFeeds Manager](http://wfm.ap.org/) installation pointed at the AP Exchange news feed
1. A working [Django](https://www.djangoproject.com/) installation
1. A cron job that inserts the AP stories resulting from the AP Exchange -> WebFeeds Manager XML into a Django database.


Then install the project requirements:

```
pip install -r requirements.txt
```

To restart
----------

If running a manual restart from `oper` account home directory on command line:
```bash
$ nohup java -jar [your_django_project]/ap_wfm/WebFeedsAgent.jar commandLine > /dev/null 2>&1 &
```
(Remember, this is only to restart. First time runinng, you must supply `userName`, `password` and `agentName`.)

To run locally
--------------

To get the ingestion script to run with a local, development set of settings:  
`python manage.py process_feed /Users/jheasly/Development/ap_wfm/WFA/feeds/All-TopHeadlines-JH/feed_644355_2015-06-02T16-39-38.445Z.xml --settings=test_root.local_settings`
