This documentation will explain how one can quickly establish events from a
Forgejo repository to be conveyed to the Fedora Messaging bus.

1. Create a webhook bind under the type **Forgejo** on the dashboard with
   a unique name and an appropriate description.

2. Navigate to the project repository on **Forgejo**.
   ![](/imgs/fogo/1.png)

3. On the **Settings** page, navigate to the **Webhooks** section.
   ![](/imgs/fogo/2.png)

4. Click on the **Add webhook** button to open the combobox.
   ![](/imgs/fogo/3.png)

5. Select the **Forgejo** option there to begin.
   ![](/imgs/fogo/4.png)

6. Fill the information accurately from the created webhook bind.
   ![](/imgs/fogo/5.png)

7. After saving, the webhook bind should be enabled.
   ![](/imgs/fogo/6.png)

8. Perform one of the following actions for triggering the events.
   1. Push (Events catalogued under the [`org.fedoraproject.prod.forgejo.push`](https://apps.fedoraproject.org/datagrepper/v2/search?topic=org.fedoraproject.prod.forgejo.push) topic)
   2. Pull request (Events catalogued under the [`org.fedoraproject.prod.forgejo.pull_request`](https://apps.fedoraproject.org/datagrepper/v2/search?topic=org.fedoraproject.prod.forgejo.pull_request) topic)
   3. Issue ticket (Events catalogued under the [`org.fedoraproject.prod.forgejo.issues`](https://apps.fedoraproject.org/datagrepper/v2/search?topic=org.fedoraproject.prod.forgejo.issues) topic)
   4. Issue comment (Events catalogued under the [`org.fedoraproject.prod.forgejo.issue_comment`](https://apps.fedoraproject.org/datagrepper/v2/search?topic=org.fedoraproject.prod.forgejo.issue_comment) topic)
   5. Action runs (Workflow executions)
      - Success (Events catalogued under the [`org.fedoraproject.prod.forgejo.action_run_success`](https://apps.fedoraproject.org/datagrepper/v2/search?topic=org.fedoraproject.prod.forgejo.action_run_success) topic)
      - Failure (Events catalogued under the [`org.fedoraproject.prod.forgejo.action_run_failure`](https://apps.fedoraproject.org/datagrepper/v2/search?topic=org.fedoraproject.prod.forgejo.action_run_failure) topic)
      - Recover (Events catalogued under the [`org.fedoraproject.prod.forgejo.action_run_recover`](https://apps.fedoraproject.org/datagrepper/v2/search?topic=org.fedoraproject.prod.forgejo.action_run_recover) topic)
      - Cancelled (Events catalogued under the [`org.fedoraproject.prod.forgejo.action_run_cancelled`](https://apps.fedoraproject.org/datagrepper/v2/search?topic=org.fedoraproject.prod.forgejo.action_run_cancelled) topic)
