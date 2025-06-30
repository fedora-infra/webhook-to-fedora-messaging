# Webhook to Fedora Messaging

## Installation

### For development

1.  Install the supported version of Python, Virtualenv, Git, Poetry and krb5-devel package on your Fedora Linux installation.
    ```
    $ sudo dnf install python3
    ```
    ```
    $ sudo dnf install virtualenv
    ```
    ```
    $ sudo dnf install git
    ```
    ```
    $ sudo dnf install poetry
    ```
    ```
    $ sudo dnf install krb5-devel
    ```

2.  Clone the repository to your local storage and make it your present working directory.
    ```
    $ git clone https://github.com/fedora-infra/webhook-to-fedora-messaging.git
    ```
    ```
    $ cd webhook-to-fedora-messaging
    ```

3.  Establish a virtual environment within the directory and activate for installing dependencies.
    ```
    $ virtualenv venv
    ```
    ```
    $ source venv/bin/activate
    ```

4.  Check the validity of the project configuration file and begin install the dependencies.
    ```
    (venv) $ poetry check
    ```
    ```
    (venv) $ poetry install
    ```

### Utilization

### For development

1.  Make sure that the virtual environment that was recently created was activated.
    ```
    $ cd webhook-to-fedora-messaging
    ```
    ```
    $ source venv/bin/activate
    ```
2.  Make a copy of the stored `logging.yaml.example` and change it to reflect your custom logging settings.
    ```
    (venv) $ cp logging.yaml.example logging.yaml
    ```
    ```
    (venv) $ nano logging.yaml
    ```
3.  Make a copy of the stored `config.example` and change it to reflect your custom application settings.
    ```
    (venv) $ cp config.example config
    ```
    ```
    (venv) $ nano config
    ```
4.  Ensure that the W2FM_CONFIG environment variable points towards the correct configuration file (e.g., `/home/user/webhook-to-fedora-messaging/config`).
5.  Start the application with the `--help` flag to understand how the application command line works.
    ```
    (venv) $ w2fm --help
    ```
    Example output
    ```
    Usage: w2fm [OPTIONS] COMMAND [ARGS]...

    Options:
      -c, --conf PATH  Read configuration from the specified module
      --version        Show the version and exit.
      --help           Show this message and exit.

    Commands:
      setup  Setup the database schema in the specified environment
    ```
6.  While pointing towards the edited config file, run the `setup` command to initialize the database.
    ```
    (venv) $ w2fm --conf config setup
    ```
    Example output
    ```
    The database has been created
    ```
7.  Note that the same command can be used to upgrade and downgrade through database schema revisions.
8.  Once the database is created, run the following command to invoke the service application.
    ```
    $ (venv) uvicorn \
               --factory "webhook_to_fedora_messaging.main:create_app" \
               --log-config logging.yaml \
               --host 0.0.0.0 \
               --port 8080 \
               --workers 4
    ```
    Example output
    ```
    [W2FM] [2024-08-14 01:56:48 +0530] [INFO] Uvicorn running on http://0.0.0.0:8080 (Press CTRL+C to quit)
    [W2FM] [2024-08-14 01:56:48 +0530] [INFO] Started parent process [11076]
    [W2FM] [2024-08-14 01:56:49 +0530] [INFO] Started server process [11081]
    [W2FM] [2024-08-14 01:56:49 +0530] [INFO] Waiting for application startup.
    [W2FM] [2024-08-14 01:56:49 +0530] [INFO] Started server process [11080]
    [W2FM] [2024-08-14 01:56:49 +0530] [INFO] Waiting for application startup.
    [W2FM] [2024-08-14 01:56:49 +0530] [INFO] Application startup complete.
    [W2FM] [2024-08-14 01:56:49 +0530] [INFO] Application startup complete.
    [W2FM] [2024-08-14 01:56:49 +0530] [INFO] Started server process [11079]
    [W2FM] [2024-08-14 01:56:49 +0530] [INFO] Waiting for application startup.
    [W2FM] [2024-08-14 01:56:49 +0530] [INFO] Application startup complete.
    [W2FM] [2024-08-14 01:56:49 +0530] [INFO] Started server process [11078]
    [W2FM] [2024-08-14 01:56:49 +0530] [INFO] Waiting for application startup.
    [W2FM] [2024-08-14 01:56:49 +0530] [INFO] Application startup complete.
    ```
    This command will make `4 workers` processes of the service available on `all interfaces` and on `port 8080`, while logging according to the configuration available in the newly created `logging.yaml` file.
9.  To stop the service application processes, invoke a keyboard interrupt by pressing `Ctrl` + `C`.
    ```
    Ctrl + C
    ```
    Example output
    ```
    ^C
    [W2FM] [2024-08-14 01:58:43 +0530] [INFO] Shutting down
    [W2FM] [2024-08-14 01:58:43 +0530] [INFO] Shutting down
    [W2FM] [2024-08-14 01:58:43 +0530] [INFO] Shutting down
    [W2FM] [2024-08-14 01:58:43 +0530] [INFO] Shutting down
    [W2FM] [2024-08-14 01:58:43 +0530] [INFO] Waiting for application shutdown.
    [W2FM] [2024-08-14 01:58:43 +0530] [INFO] Waiting for application shutdown.
    [W2FM] [2024-08-14 01:58:43 +0530] [INFO] Waiting for application shutdown.
    [W2FM] [2024-08-14 01:58:43 +0530] [INFO] Application shutdown complete.
    [W2FM] [2024-08-14 01:58:43 +0530] [INFO] Application shutdown complete.
    [W2FM] [2024-08-14 01:58:43 +0530] [INFO] Application shutdown complete.
    [W2FM] [2024-08-14 01:58:43 +0530] [INFO] Finished server process [11079]
    [W2FM] [2024-08-14 01:58:43 +0530] [INFO] Finished server process [11078]
    [W2FM] [2024-08-14 01:58:43 +0530] [INFO] Finished server process [11081]
    [W2FM] [2024-08-14 01:58:43 +0530] [INFO] Waiting for application shutdown.
    [W2FM] [2024-08-14 01:58:43 +0530] [INFO] Application shutdown complete.
    [W2FM] [2024-08-14 01:58:43 +0530] [INFO] Finished server process [11080]
    [W2FM] [2024-08-14 01:58:43 +0530] [INFO] Received SIGINT, exiting.
    [W2FM] [2024-08-14 01:58:43 +0530] [INFO] Terminated child process [11078]
    [W2FM] [2024-08-14 01:58:43 +0530] [INFO] Terminated child process [11079]
    [W2FM] [2024-08-14 01:58:43 +0530] [INFO] Terminated child process [11080]
    [W2FM] [2024-08-14 01:58:43 +0530] [INFO] Terminated child process [11081]
    [W2FM] [2024-08-14 01:58:43 +0530] [INFO] Waiting for child process [11078]
    [W2FM] [2024-08-14 01:58:43 +0530] [INFO] Waiting for child process [11079]
    [W2FM] [2024-08-14 01:58:43 +0530] [INFO] Waiting for child process [11080]
    [W2FM] [2024-08-14 01:58:43 +0530] [INFO] Waiting for child process [11081]
    [W2FM] [2024-08-14 01:58:43 +0530] [INFO] Stopping parent process [11076]
    ```
10. For more utility options on running the service, start `uvicorn` with the `--help` flag.
    ```
    (venv) $ uvicorn --help
    ```
    Example output
    ```
    Usage: uvicorn [OPTIONS] APP

    Options:
      --host TEXT                     Bind socket to this host.  [default:
                                      127.0.0.1]
      --port INTEGER                  Bind socket to this port. If 0, an available
                                      port will be picked.  [default: 8000]
      --uds TEXT                      Bind to a UNIX domain socket.
      --fd INTEGER                    Bind to socket from this file descriptor.
    ...
    ```
11. Deactivate the virtual environment by running the following command.
    ```
    (venv) $ deactivate
    ```

## From cookiecutter template

This is where you describe Webhook to Fedora Messaging.

The full documentation is [on ReadTheDocs](https://webhook-to-fedora-messaging.readthedocs.io).

You can install it [from PyPI](https://pypi.org/project/webhook-to-fedora-messaging/).

![PyPI](https://img.shields.io/pypi/v/webhook-to-fedora-messaging.svg)
![Supported Python versions](https://img.shields.io/pypi/pyversions/webhook-to-fedora-messaging.svg)
![Build status](http://github.com/fedora-infra/webhook-to-fedora-messaging/actions/workflows/main.yml/badge.svg?branch=develop)
![Documentation](https://readthedocs.org/projects/webhook-to-fedora-messaging/badge/?version=latest)
