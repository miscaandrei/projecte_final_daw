import os
import sys

sys.path.append('/home/ikarus_app/web/projecte_final_daw/ikarus_base/')


os.environ['DJANGO_SETTINGS_MODULE'] = 'ikarus_base.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()



