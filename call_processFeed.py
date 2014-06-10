#!/Users/jheasly/.virtualenvs/test_root/bin/python

def main():
    import os, sys
    from os import environ
    # Adds parent of wherever file is to sys.path:
    sys.path.append(os.path.join(os.path.abspath(os.path.dirname(__file__)),
                             '..'))
    sys.path.append(os.path.join(os.path.abspath(os.path.dirname(__file__)),
                             '../test_root'))
    environ['DJANGO_SETTINGS_MODULE'] = 'test_root.settings'
    
    if len(sys.argv) > 1:
        path_to_xml = sys.argv[1]
        
        from django.core import management
        management.call_command('processFeed', path_to_xml)
    else:
        raise ValueError('Need to supply a path to XML file.')

if __name__ == "__main__": main()
