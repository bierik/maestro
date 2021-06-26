import os

from configurations import Configuration, values


class Base(Configuration):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    SECRET_KEY = values.Value("secret")
    ALLOWED_HOSTS = ["localhost"]
    INSTALLED_APPS = [
        "django.contrib.admin",
        "django.contrib.auth",
        "django.contrib.contenttypes",
        "django.contrib.sessions",
        "django.contrib.messages",
        "django.contrib.staticfiles",
        "django_extensions",
        "colorfield",
        "recurrence",
        "rest_framework",
        "storages",
        "customer",
        "task",
        "report",
        "invoice",
        "flat",
        "api",
    ]
    MIDDLEWARE = [
        "django.middleware.security.SecurityMiddleware",
        "django.contrib.sessions.middleware.SessionMiddleware",
        "django.middleware.common.CommonMiddleware",
        "django.middleware.csrf.CsrfViewMiddleware",
        "django.contrib.auth.middleware.AuthenticationMiddleware",
        "django.contrib.messages.middleware.MessageMiddleware",
        "django.middleware.clickjacking.XFrameOptionsMiddleware",
    ]
    ROOT_URLCONF = "maestro.urls"
    WSGI_APPLICATION = "maestro.wsgi.application"

    DATABASE_NAME = values.Value("maestro_development")
    DATABASE_ENGINE = values.Value("django.db.backends.postgresql_psycopg2")
    DATABASE_USER = values.Value("")
    DATABASE_PASSWORD = values.Value("")
    DATABASE_HOST = values.Value("localhost")
    DATABASE_PORT = values.Value("")
    DATABASE_OPTIONS = values.DictValue({})

    @property
    def DATABASES(self):
        return {
            "default": {
                "ENGINE": self.DATABASE_ENGINE,
                "NAME": self.DATABASE_NAME,
                "USER": self.DATABASE_USER,
                "PASSWORD": self.DATABASE_PASSWORD,
                "HOST": self.DATABASE_HOST,
                "PORT": self.DATABASE_PORT,
                "OPTIONS": self.DATABASE_OPTIONS,
                "ATOMIC_REQUESTS": True,
            }
        }

    AUTH_PASSWORD_VALIDATORS = [
        {
            "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"  # noqa
        },
        {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
        {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
        {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
    ]

    DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

    LANGUAGE_CODE = "de-CH"
    USE_I18N = True
    USE_L10N = True
    USE_TZ = True
    TIME_ZONE = "Europe/Zurich"

    STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]

    X_FRAME_OPTIONS = "ALLOWALL"

    TEMPLATES = [
        {
            "BACKEND": "django.template.backends.django.DjangoTemplates",
            "APP_DIRS": True,
            "OPTIONS": {
                "context_processors": [
                    "django.template.context_processors.debug",
                    "django.template.context_processors.request",
                    "django.contrib.auth.context_processors.auth",
                    "django.contrib.messages.context_processors.messages",
                ],
            },
        },
    ]

    LOGGING = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "verbose": {
                "format": (
                    "%(asctime)s [%(process)d] [%(levelname)s] "
                    "pathname=%(pathname)s lineno=%(lineno)s "
                    "funcname=%(funcName)s %(message)s"
                ),
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
            "simple": {"format": "%(levelname)s %(message)s"},
        },
        "handlers": {
            "null": {
                "level": "DEBUG",
                "class": "logging.NullHandler",
            },
            "console": {
                "level": "INFO",
                "class": "logging.StreamHandler",
                "formatter": "verbose",
            },
        },
        "loggers": {
            "django": {
                "handlers": ["console"],
                "level": "DEBUG",
                "propagate": True,
            },
            "django.request": {
                "handlers": ["console"],
                "level": "DEBUG",
                "propagate": False,
            },
        },
    }


class Development(Base):
    DEBUG = True
    STATIC_URL = "/staticfiles/"

    @property
    def STATIC_ROOT(self):
        return os.path.join(self.BASE_DIR, "staticfiles")

    MEDIA_URL = "/media/"

    def MEDIA_ROOT(self):
        return os.path.join(self.BASE_DIR, "media")

    WEASYPRINT_HOST = "localhost"


class Production(Base):
    # SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    # SECURE_SSL_REDIRECT = True
    ALLOWED_HOSTS = values.ListValue([])
    AWS_ACCESS_KEY_ID = values.Value("")
    AWS_SECRET_ACCESS_KEY = values.Value("")
    AWS_STORAGE_BUCKET_NAME = "putztrix-maestro-bucket"
    AWS_S3_REGION_NAME = "eu-central-1"
    AWS_DEFAULT_ACL = None
    AWS_S3_SIGNATURE_VERSION = "s3v4"
    AWS_S3_CUSTOM_DOMAIN = f"{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com"
    AWS_S3_OBJECT_PARAMETERS = {
        "CacheControl": "max-age=86400",
    }
    STATIC_LOCATION = "static"
    STATIC_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/{STATIC_LOCATION}/"
    STATICFILES_STORAGE = "invoice.storage_backends.StaticStorage"

    DEFAULT_FILE_STORAGE = "invoice.storage_backends.MediaStorage"

    PRIVATE_MEDIA_LOCATION = "media"
    PRIVATE_FILE_STORAGE = "invoice.storage_backends.MediaStorage"

    WEASYPRINT_HOST = "weasyprint"

    X_FRAME_OPTIONS = "SAMEORIGIN"
