# The database URL schema using synchronous processing (consisting of username, password and port)
# database_url = "sqlite:////tmp/w2fm-rewrite.db"
database_url = "postgresql+asyncpg://w2fm:w2fm@192.168.0.212:5430/w2fm"

# The location of serving the application service
service_host = "0.0.0.0"  # noqa : S104

# The port on which the application service is hosted
service_port = 8080

# Automatically reload if the code is changed
reload_on_change = True

# The default configuration for service logging
main_logger_conf = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": "[W2FM] %(asctime)s [%(levelname)s] %(message)s",
            "datefmt": "[%Y-%m-%d %I:%M:%S %z]",
        },
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "formatter": "standard",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
        },
    },
    "root": {
        "level": "DEBUG",
        "handlers": ["console"],
    },
}

# The default configuration for WSGI logging
wsgi_logger_conf = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": "[W2FM] %(asctime)s [%(levelname)s] %(message)s",
            "datefmt": "[%Y-%m-%d %I:%M:%S %z]",
            "use_colors": None,
        },
        "access": {
            "()": "uvicorn.logging.AccessFormatter",
            "fmt": (
                "[W2FM] %(asctime)s [%(levelname)s] %(client_addr)s"
                " - '%(request_line)s' %(status_code)s"
            ),
            "datefmt": "[%Y-%m-%d %I:%M:%S %z]",
        },
    },
    "handlers": {
        "default": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
        },
        "access": {
            "formatter": "access",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
        },
    },
    "loggers": {
        "uvicorn": {"handlers": ["default"], "level": "INFO", "propagate": False},
        "uvicorn.error": {"level": "INFO"},
        "uvicorn.access": {"handlers": ["access"], "level": "INFO", "propagate": False},
    },
}
