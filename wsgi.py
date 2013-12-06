from django.core.wsgi import get_wsgi_application
from django.static import Cling

application = Cling(get_wsgi_application())
