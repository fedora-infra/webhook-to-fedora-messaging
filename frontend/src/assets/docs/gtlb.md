This documentation will explain how one can quickly establish events from a
GitLab repository to be conveyed to the Fedora Messaging bus.

1. Create a webhook bind under the type **GitLab** on the dashboard with
   a unique name and an appropriate description.

2. From the navigation menu, head over to the **Webhooks** page from the **Settings** section.
   ![](/imgs/gtlb/1.png)

3. Click on the **Add new webhook** button.
   ![](/imgs/gtlb/2.png)

4. Fill the information accurately from the created webhook bind.
   ![](/imgs/gtlb/3.png)

5. Select all applicable events for triggering the webhook.
   ![](/imgs/gtlb/4.png)

6. Click on the **Add webhook** button to save changes.
   ![](/imgs/gtlb/5.png)

7. After saving, the webhook bind should be enabled.
   ![](/imgs/gtlb/6.png)

8. Perform one of the following actions for triggering the events.
   1. Push (Events catalogued under the [`org.fedoraproject.prod.gitlab.push`](https://apps.fedoraproject.org/datagrepper/v2/search?topic=org.fedoraproject.prod.gitlab.push) topic)
   2. Pull request (Events catalogued under the [`org.fedoraproject.prod.gitlab.pull_request`](https://apps.fedoraproject.org/datagrepper/v2/search?topic=org.fedoraproject.prod.gitlab.pull_request) topic)
   3. Issue ticket (Events catalogued under the [`org.fedoraproject.prod.gitlab.issues`](https://apps.fedoraproject.org/datagrepper/v2/search?topic=org.fedoraproject.prod.gitlab.issues) topic)
   4. Issue comment (Events catalogued under the [`org.fedoraproject.prod.gitlab.issue_comment`](https://apps.fedoraproject.org/datagrepper/v2/search?topic=org.fedoraproject.prod.gitlab.issue_comment) topic)
