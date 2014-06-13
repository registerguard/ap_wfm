#!/usr/bin/env python
def main():
    import os, sys
    from os import environ
    '''
    Adds parent of call_process_feed.py to sys.path:
    
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
