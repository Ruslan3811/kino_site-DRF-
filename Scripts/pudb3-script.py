#!c:\users\ruslan\dev\11_projs\drf_kino_site\scripts\python.exe
# EASY-INSTALL-ENTRY-SCRIPT: 'pudb==2021.2.2','console_scripts','pudb3'
__requires__ = 'pudb==2021.2.2'
import re
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(
        load_entry_point('pudb==2021.2.2', 'console_scripts', 'pudb3')()
    )
