This documentation will explain how to relay events from Pretix to the Fedora Messaging bus.

1. Create a webhook bind under the type **Pretix** on the dashboard with
   a unique name and an appropriate description.

2. Follow the [Pretix documentation on Webhooks](https://docs.pretix.eu/dev/api/webhooks.html#webhooks)
   to setup a webhook in your Pretix instance.

3. Fill the target URL accurately from the created webhook bind. There is no token field for Pretix at the moment

4. After saving, the webhook bind should be enabled.
