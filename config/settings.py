

from pathlib import Path

from decouple import config, Csv


# ============================================================
# BASE
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent


# ============================================================
# SECURITY
# ============================================================

SECRET_KEY = config("SECRET_KEY")

DEBUG = config(
    "DEBUG",
    default=True,
    cast=bool,
)

ALLOWED_HOSTS = config(
    "ALLOWED_HOSTS",
    default="127.0.0.1,localhost",
    cast=Csv(),
)


# ============================================================
# APPLICATIONS
# ============================================================

INSTALLED_APPS = [
    # Django
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Project applications
    "apps.accounts.apps.AccountsConfig",
    "apps.products.apps.ProductsConfig",
    "apps.shops.apps.ShopsConfig",
    "apps.cart.apps.CartConfig",
    "apps.orders.apps.OrdersConfig",
    "apps.payments",
    "apps.reviews",
    "apps.ai.apps.AIConfig",
    "apps.dashboard.apps.DashboardConfig",
]


# ============================================================
# MIDDLEWARE
# ============================================================

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


# ============================================================
# URL / SERVER
# ============================================================

ROOT_URLCONF = "config.urls"

WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi.application"


# ============================================================
# TEMPLATES
# ============================================================

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",

        "DIRS": [
            BASE_DIR / "templates",
        ],

        "APP_DIRS": True,

        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]


# ============================================================
# DATABASE
# ============================================================

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# ============================================================
# AUTHENTICATION
# ============================================================

AUTH_USER_MODEL = "accounts.User"

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "UserAttributeSimilarityValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "MinimumLengthValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "CommonPasswordValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "NumericPasswordValidator"
        ),
    },
]

LOGIN_URL = "/accounts/login/"
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/accounts/login/"


# ============================================================
# INTERNATIONALIZATION
# ============================================================

LANGUAGE_CODE = "en-us"

TIME_ZONE = config(
    "TIME_ZONE",
    default="UTC",
)

USE_I18N = True
USE_TZ = True


# ============================================================
# STATIC FILES
# ============================================================

STATIC_URL = "/static/"

STATICFILES_DIRS = [
    BASE_DIR / "static",
]

STATIC_ROOT = BASE_DIR / "staticfiles"


# ============================================================
# MEDIA FILES
# ============================================================

MEDIA_URL = "/media/"

MEDIA_ROOT = BASE_DIR / "media"


# ============================================================
# CSRF
# ============================================================

CSRF_TRUSTED_ORIGINS = config(
    "CSRF_TRUSTED_ORIGINS",
    default="",
    cast=Csv(),
)


# ============================================================
# EMAIL
# ============================================================

EMAIL_BACKEND = config(
    "EMAIL_BACKEND",
    default="django.core.mail.backends.console.EmailBackend",
)

DEFAULT_FROM_EMAIL = config(
    "DEFAULT_FROM_EMAIL",
    default="webmaster@localhost",
)


# ============================================================
# PAYMENT CONFIGURATION
# ============================================================

# ------------------------------------------------------------
# Chapa
# ------------------------------------------------------------

CHAPA_SECRET_KEY = config(
    "CHAPA_SECRET_KEY",
    default="",
)

CHAPA_PUBLIC_KEY = config(
    "CHAPA_PUBLIC_KEY",
    default="",
)

CHAPA_CALLBACK_URL = config(
    "CHAPA_CALLBACK_URL",
    default="",
)



CHAPA_WEBHOOK_SECRET = config(
    "CHAPA_WEBHOOK_SECRET",
    default="",
)


# ------------------------------------------------------------
# Telebirr
# ------------------------------------------------------------

TELEBIRR_APP_ID = config(
    "TELEBIRR_APP_ID",
    default="",
)

TELEBIRR_APP_KEY = config(
    "TELEBIRR_APP_KEY",
    default="",
)

TELEBIRR_CALLBACK_URL = config(
    "TELEBIRR_CALLBACK_URL",
    default="",
)



TELEBIRR_WEBHOOK_SECRET = config(
    "TELEBIRR_WEBHOOK_SECRET",
    default="",
)


# ------------------------------------------------------------
# Stripe
# ------------------------------------------------------------

STRIPE_SECRET_KEY = config(
    "STRIPE_SECRET_KEY",
    default="",
)

STRIPE_PUBLIC_KEY = config(
    "STRIPE_PUBLIC_KEY",
    default="",
)

STRIPE_WEBHOOK_SECRET = config(
    "STRIPE_WEBHOOK_SECRET",
    default="",
)


# ------------------------------------------------------------
# PayPal
# ------------------------------------------------------------

PAYPAL_CLIENT_ID = config(
    "PAYPAL_CLIENT_ID",
    default="",
)

PAYPAL_CLIENT_SECRET = config(
    "PAYPAL_CLIENT_SECRET",
    default="",
)

PAYPAL_MODE = config(
    "PAYPAL_MODE",
    default="sandbox",
)

PAYPAL_ENVIRONMENT = config(
    "PAYPAL_ENVIRONMENT",
    default=PAYPAL_MODE,
)

PAYPAL_RETURN_URL = config(
    "PAYPAL_RETURN_URL",
    default="",
)

PAYPAL_CANCEL_URL = config(
    "PAYPAL_CANCEL_URL",
    default="",
)

PAYPAL_WEBHOOK_SECRET = config(
    "PAYPAL_WEBHOOK_SECRET",
    default="",
)


CHAPA_RETURN_URL = config(
    "CHAPA_RETURN_URL",
    default="http://127.0.0.1:8000/payments/success/",
)

TELEBIRR_RETURN_URL = config(
    "TELEBIRR_RETURN_URL",
    default="http://127.0.0.1:8000/payments/success/",
)

TELEBIRR_BASE_URL = config(
    "TELEBIRR_BASE_URL",
    default="",
)

TELEBIRR_MERCHANT_ID = config(
    "TELEBIRR_MERCHANT_ID",
    default="",
)

TELEBIRR_PRIVATE_KEY = config(
    "TELEBIRR_PRIVATE_KEY",
    default="",
)

TELEBIRR_PUBLIC_KEY = config(
    "TELEBIRR_PUBLIC_KEY",
    default="",
)

PAYPAL_RETURN_URL = config(
    "PAYPAL_RETURN_URL",
    default="http://127.0.0.1:8000/payments/success/",
)

PAYPAL_CANCEL_URL = config(
    "PAYPAL_CANCEL_URL",
    default="http://127.0.0.1:8000/payments/cancel/",
)

PAYPAL_ENVIRONMENT = config(
    "PAYPAL_ENVIRONMENT",
    default="sandbox",
)


# ============================================================
# AI CONFIGURATION
# ============================================================

OPENAI_API_KEY = config(
    "OPENAI_API_KEY",
    default="",
)



GEMINI_API_KEY = config(
    "GEMINI_API_KEY",
    default="",
)

GEMINI_MODEL = config(
    "GEMINI_MODEL",
    default="gemini-2.5-flash-lite",
)


# ============================================================
# DEFAULT PRIMARY KEY
# ============================================================

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

