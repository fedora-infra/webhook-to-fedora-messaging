This documentation will explain how one can quickly establish events from a
Discourse to be conveyed to the Fedora Messaging bus.

1. Create a webhook bind under the type **Discourse** on the dashboard with
   a unique name and an appropriate description.

2. In the Discourse Admin section, look for webhooks in the lateral bar.

3. Click on the **Add Webhook** button.
   ![](/imgs/discourse/1.png)

4. Enter the Payload URL from the created webhook's Endpoint field.

5. Content type should be `application/json`.

6. Enter the secret from the webhook bind's Token field.

7. Select the events you want to relay on the Fedora Messaging bus.
   ![](/imgs/discourse/2.png)

8. Enable the TLS certificate check, set the `Active` checkbox and click `Create`.
   ![](/imgs/discourse/3.png)

9. The Discourse events should now be relayed on the Fedora Messaging bus.
