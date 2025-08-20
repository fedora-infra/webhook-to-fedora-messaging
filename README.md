# Webhook to Fedora Messaging

## Installation

1.  Install the project dependencies on your Fedora Linux installation.
    ```
    $ sudo dnf install --setopt=install_weak_deps=False python3 git poetry npm
    ```
    ```
    $ sudo dnf install --setopt=install_weak_deps=False ansible krb5-devel supervisor
    ```

2.  Clone the TinyStage repository to your local storage and make it your
    present working directory.
    ```
    $ git clone https://github.com/fedora-infra/tiny-stage.git
    ```
    ```
    $ cd tiny-stage
    ```

3.  Setup the `ipa` and `auth` VM environments using TinyStage for service
    authentication by the project.
    ```
    $ vagrant up ipa
    ```
    ```
    $ vagrant up auth
    ```

4.  Clone the project separately to your local storage and make it your
    present working directory.
    ```
    $ git clone https://github.com/fedora-infra/webhook-to-fedora-messaging.git
    ```
    ```
    $ cd webhook-to-fedora-messaging
    ```

## Utilization

1.  Start the development environment once the TinyStage's `ipa` and `auth`
    VMs are initialized.
    ```
    $ ansible-playbook ./devel/ansible/devel.yml
    ```
    ```
    [WARNING]: provided hosts list is empty, only localhost is available. Note that the implicit localhost does not match 'all'
    PLAY [localhost] *************************************************************************************************

    TASK [Gathering Facts] *******************************************************************************************
    ok: [localhost]

    TASK [local : Install the backend] *******************************************************************************
    changed: [localhost]

    TASK [local : Get the Tinystage CA cert] *************************************************************************
    ok: [localhost]

    TASK [local : Load the content of the Tinystage CA cert] *********************************************************
    ok: [localhost]

    TASK [local : Find where certifi's CA bundle is located] *********************************************************
    ok: [localhost]

    TASK [local : Put tinystage root CA in the list of CA's for certifi] *********************************************
    ok: [localhost]

    TASK [local : Register the application with the OIDC provider] ***************************************************
    ok: [localhost]

    TASK [local : Load the OIDC config] ******************************************************************************
    ok: [localhost]

    TASK [local : Extract the OIDC client_id] ************************************************************************
    ok: [localhost]

    TASK [local : Create the backend config file] ********************************************************************
    ok: [localhost]

    TASK [local : Create the frontend config file] *******************************************************************
    ok: [localhost]

    TASK [local : Create or update the database] *********************************************************************
    ok: [localhost]

    TASK [local : Create the supervisord config file] ****************************************************************
    ok: [localhost]

    TASK [local : Start supervisord] *********************************************************************************
    ok: [localhost]

    TASK [local : Install the frontend] ******************************************************************************
    ok: [localhost]

    PLAY RECAP *******************************************************************************************************
    localhost                  : ok=15   changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
    ```

2.  Check the status of the running backend service and frontend service using
    the following command.
    ```
    $ supervisorctl status
    ```
    ```
    backend                          RUNNING   pid 1234, uptime 00:00:00
    frontend                         RUNNING   pid 5678, uptime 00:00:00
    ```

3.  The frontend and the backend services should now be running locally on the
    following addresses.
    ```
    Frontend -> http://localhost:5173/
    ```
    ```
    Backend -> http://localhost:8000/
    ```

4.  The backend and frontend logs are stored locally and can be followed using
    the following command.
    ```
    -rw-r--r--. 1 tinyhost tinyhost 810K Aug 20 10:42 backend.log
    -rw-r--r--. 1 tinyhost tinyhost  18K Aug 20 10:55 frontend.log
    -rw-r--r--. 1 tinyhost tinyhost 3.5K Aug 20 10:42 supervisord.log
    ```
    ```
    $ tail -f devel/*.log
    ```

5.  You can stop the backend and frontend services when you are done with using
    the following command.
    ```
    $ supervisorctl stop backend
    ```
    ```
    $ supervisorctl stop frontend
    ```

6.  The backend configuration is stored locally and changes to the schema can
    be applied using this.
    ```
    $ nano devel/w2fm.cfg
    ```
    ```
    $ W2FM_CONFIG=devel/w2fm.cfg poetry run w2fm setup
    ```

7.  Create a virtual environment and install the dependencies associated with
    the backend inside of it.
    ```
    $ python3 -m venv venv
    ```
    ```
    $ source venv/bin/activate
    ```

8.  The testcases associated with the backend codebase can be executed in an
    activated virtual environment.
    ```
    (venv) $ tox -e py313
    ```
    ```
    tests/test_cli.py:
      ✓ Creating a service using CLI

    tests/test_message/test_message_create.py:
      ✓ Sending data and successfully creating message[github-push]
      » Sending data and successfully creating message[github-pull request]
      ✓ Sending data and successfully creating message[gitlab-push]
      ✓ Sending data and successfully creating message[gitlab-pull request]
      ✓ Sending data and successfully creating message[forgejo-push]
      » Sending data and successfully creating message[forgejo-pull request]
      ✓ Sending data but facing broken connection[github-push]
      » Sending data but facing broken connection[github-pull request]
      ✓ Sending data but facing broken connection[gitlab-push]
      ✓ Sending data but facing broken connection[gitlab-pull request]
      ✓ Sending data but facing broken connection[forgejo-push]
      » Sending data but facing broken connection[forgejo-pull request]
      ✓ Sending data with wrong information[github-push]
      » Sending data with wrong information[github-pull request]
      » Sending data with wrong information[gitlab-push]
      » Sending data with wrong information[gitlab-pull request]
      ✓ Sending data with wrong information[forgejo-push]
      » Sending data with wrong information[forgejo-pull request]
      ✓ Sending data to a non-existent service                                                                                                                                                                                                                                                                                                                                     ✓ Sending data with wrong format[github]
      ✓ Sending data with wrong format[gitlab]
      ✓ Sending data with wrong format[forgejo]
      ✓ Ignoring username lookups on bot actions[github-push]
      » Ignoring username lookups on bot actions[github-pull request]
      » Ignoring username lookups on bot actions[gitlab-push]
      » Ignoring username lookups on bot actions[gitlab-pull request]
      » Ignoring username lookups on bot actions[forgejo-push]
      » Ignoring username lookups on bot actions[forgejo-pull request]

    tests/test_service/test_service_create.py:
      ✓ Creating a non-existent service with wrong information[GitHub repository with name]
      ✓ Creating a non-existent service with wrong information[GitHub repository without name]
      ✓ Creating a non-existent service with wrong information[Forgejo repository with name]
      ✓ Creating a non-existent service with wrong information[Forgejo repository without name]
      ✓ Creating a non-existent service with wrong information[Gitlab repository with name]
      ✓ Creating a non-existent service with wrong information[Gitlab repository without name]
      ✓ Creating an existing service again

    tests/test_service/test_service_get.py:
      ✓ Spotting an existing service
      ✓ Spotting a non-existent service

    tests/test_service/test_service_list.py:
      ✓ Listing all available services

    tests/test_service/test_service_refresh.py:
      ✓ Regenerating access token of an existing service
      ✓ Regenerating access token of a non-existent service

    tests/test_service/test_service_revoke.py:
      ✓ Revoking an existing service
      ✓ Revoking a non-existent service

    tests/test_service/test_service_update.py:
      ✓ Updating an existing service
      ✓ Updating an existing user
      ✓ Verifying an existing user uniqueness during update
      ✓ Transferring an existing service to a non-existent user
      ✓ Updating a non-existent service
      ✓ Updating an existing service with invalid data

    tests/test_user/test_user_get.py:
      ✓ Spotting users[Existing]
      ✓ Spotting users[Non-existent]
      ✓ Spotting myself

    tests/test_user/test_user_search.py:
      ✓ Searching users with valid format
      ✓ Searching users with wrong format
    ```

9.  The typechecks associated with the backend codebase can be executed in an
    activated virtual environment.
    ```
    (venv) $ tox -e types
    ```
    ```
    types: commands_pre[0]> poetry install --all-extras
    Installing dependencies from lock file
    No dependencies to install or update
    Installing the current project: webhook-to-fedora-messaging (0.2.1)
    types: commands[0]> poetry run mypy webhook_to_fedora_messaging tests
    Success: no issues found in 59 source files
    types: commands[1]> poetry run pyright webhook_to_fedora_messaging tests
    0 errors, 0 warnings, 0 informations
      types: OK (12.33=setup[0.07]+cmd[1.84,1.42,9.01] seconds)
      congratulations :) (12.43 seconds)
    ```

10. The formatting associated of the project codebase can be executed in an
    activate virtual environment.
    ```
    (venv) $ tox -e checks
    ```
    ```
    checks: commands_pre[0]> poetry install --all-extras
    Installing dependencies from lock file
    No dependencies to install or update
    Installing the current project: webhook-to-fedora-messaging (0.2.1)
    checks: commands[0]> pre-commit run --all-files
    trim trailing whitespace.................................................Passed
    fix end of files.........................................................Passed
    check yaml...............................................................Passed
    check for added large files..............................................Passed
    black....................................................................Passed
    ruff (legacy alias)......................................................Passed
    rstcheck.................................................................Passed
    Run prettier.............................................................Passed
    Run the JS linter........................................................Passed
      checks: OK (12.76=setup[0.06]+cmd[1.77,10.93] seconds)
      congratulations :) (12.86 seconds)
    ```

11. The documentation associated with the project repository can be built in an
    activated virtual environment.
    ```
    (venv) $ tox -e docs
    ```
    ```
    docs: commands_pre[0] /home/tinyhost/Projects/webhook-to-fedora-messaging/docs> poetry install --all-extras
    Installing dependencies from lock file
    No dependencies to install or update
    Installing the current project: webhook-to-fedora-messaging (0.2.1)
    docs: commands[0] /home/tinyhost/Projects/webhook-to-fedora-messaging/docs> mkdir -p _static
    docs: commands[1] /home/tinyhost/Projects/webhook-to-fedora-messaging/docs> rm -rf _build
    docs: commands[2] /home/tinyhost/Projects/webhook-to-fedora-messaging/docs> rm -rf _source
    docs: commands[3] /home/tinyhost/Projects/webhook-to-fedora-messaging/docs> poetry run sphinx-build -W -b html -d /home/tinyhost/Projects/webhook-to-fedora-messaging/.tox/docs/tmp/doctrees . _build/html
      docs: OK (13.87=setup[0.07]+cmd[1.74,0.00,0.01,0.00,12.05] seconds)
      congratulations :) (13.97 seconds)
    ```

12. Move into the frontend directory to work on developing, managing and
    testing the frontend codebase.
    ```
    $ cd frontend
    ```
    ```
    $ npm install
    ```

13. Improve the codebase quality and enforce the functional styling by
    executing the following command.
    ```
    $ npm run lint
    ```
    ```
    > frontend@0.1.0 lint
    > eslint .
    ```

14. Enforce the codebase consistency and check for potential errors by
    executing the following command.
    ```
    $ npm run format
    ```
    ```
    > frontend@0.1.0 format
    > prettier --write .

    dist/assets/index-DUQL2yBM.js 4475ms (unchanged)
    dist/assets/index-DWYtoH4_.css 1228ms (unchanged)
    dist/index.html 54ms (unchanged)
    eslint.config.js 11ms (unchanged)
    index.html 7ms (unchanged)
    package-lock.json 117ms (unchanged)
    package.json 2ms (unchanged)
    src/assets/docs/fogo.md 64ms (unchanged)
    src/assets/docs/gthb.md 13ms (unchanged)
    src/assets/docs/gtlb.md 13ms (unchanged)
    src/components/call.jsx 12ms (unchanged)
    src/components/code.jsx 16ms (unchanged)
    src/components/diff.jsx 6ms (unchanged)
    src/components/edit.jsx 13ms (unchanged)
    src/components/fact.jsx 4ms (unchanged)
    src/components/flag.jsx 6ms (unchanged)
    src/components/flaw.jsx 4ms (unchanged)
    src/components/list.jsx 8ms (unchanged)
    src/components/make.jsx 12ms (unchanged)
    src/components/mode.jsx 4ms (unchanged)
    src/components/navi.jsx 12ms (unchanged)
    src/components/side.jsx 9ms (unchanged)
    src/components/unit.jsx 15ms (unchanged)
    src/components/wipe.jsx 9ms (unchanged)
    src/config/data.js 3ms (unchanged)
    src/config/oidc.js 3ms (unchanged)
    src/features/api.js 5ms (unchanged)
    src/features/auth.jsx 7ms (unchanged)
    src/features/data.jsx 2ms (unchanged)
    src/features/part.jsx 7ms (unchanged)
    src/main.jsx 5ms (unchanged)
    src/styles/core.css 9ms (unchanged)
    vite.config.js 3ms (unchanged)
    ```
