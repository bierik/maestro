import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "maestro.settings")

from configurations.wsgi import get_wsgi_application  # noqa

application = get_wsgi_application()
