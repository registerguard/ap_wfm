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
$ nohup java -jar projects_root/ap_wfm/WebFeedsAgent.jar commandLine > /dev/null 2>&1 &
```
