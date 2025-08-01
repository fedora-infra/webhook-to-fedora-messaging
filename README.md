# Webhook to Fedora Messaging

## Installation

### For development

1.  Install the supported version of Python, Virtualenv, Git, Poetry and krb5-devel package on your Fedora Linux installation.

    ```
    $ sudo dnf install --setopt=install_weak_deps=false python3 git poetry krb5-devel ansible supervisor npm
    ```

2.  Clone and run TinyStage, a local staging environment for authentication and common services.

    ```
    $ git clone https://github.com/fedora-infra/tiny-stage.git
    $ cd tiny-stage
    $ vagrant up ipa auth
    ```

    If you've never run TinyStage before, this step will take a while.

3.  Clone the repository to your local storage and make it your present working directory.

    ```
    $ cd ..
    $ git clone https://github.com/fedora-infra/webhook-to-fedora-messaging.git
    $ cd webhook-to-fedora-messaging
    ```

### Utilization

### For development

Setup the development environment. For this step to complete, you will need to have TinyStage's `ipa` and `auth` VMs running.

```
$ ansible-playbook ./devel/ansible/devel.yml
```

The backend and the frontend are now running. You can check their status with:

```
$ supervisorctl status
```

You can follow the backend and the frontend logs with:

```
$ tail -f devel/*.log
```

You can stop the backend and the frontend with:

```
$ supervisorctl stop
```

The backend configuration file for development is `devel/w2fm.cfg`.
If you make changes to the schema, you can apply the migrations with:

```
$ W2FM_CONFIG=devel/w2fm.cfg poetry run w2fm setup
```

You can run the Javascript linter with:

```
$ cd frontend
$ npm run lint
```
