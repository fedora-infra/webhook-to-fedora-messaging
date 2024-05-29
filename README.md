# Webhook to Fedora Messaging

## Installation

### For development

1.  Install the supported version of Python, Virtualenv, Git and Poetry on your Fedora Linux installation.
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

## From cookiecutter template

This is where you describe Webhook to Fedora Messaging.

The full documentation is [on ReadTheDocs](https://webhook-to-fedora-messaging.readthedocs.io).

You can install it [from PyPI](https://pypi.org/project/webhook-to-fedora-messaging/).

![PyPI](https://img.shields.io/pypi/v/webhook-to-fedora-messaging.svg)
![Supported Python versions](https://img.shields.io/pypi/pyversions/webhook-to-fedora-messaging.svg)
![Build status](http://github.com/fedora-infra/webhook-to-fedora-messaging/actions/workflows/main.yml/badge.svg?branch=develop)
![Documentation](https://readthedocs.org/projects/webhook-to-fedora-messaging/badge/?version=latest)
