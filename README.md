# WOKO.CH Discord-Webhook

Checking https://woko.ch for new rooms so you don't have to.



## Setup

##### 1.  Creating the Webhook:

`Discord Server > Server Settings > Integrations > View Webhooks / Create Webhook > New Webhook`

Name the webhook anything you like and pick a channel, where it will send the notifications.

Click `Copy Webhook URL` and copy that URL into `config.cfg` under `webhook_urls`

```ini
[woko-bot]
wait_time = 45

[webhook_urls]
;Add webhooks here with syntax: {name} = {discord url}
my_hook = https://discord.com/api/webhooks/xxx/XXX
```

You can also set the time that the bot waits between page-refreshes in seconds.



#### 2. Running the bot:

Install packages:

```bash
$ pip3 install -r requirements.txt
```

Run the webhook:

```bash
$ python3 main.py
```

The bot will repeatedly scan https://woko.ch/en/zimmer-in-zuerich for changes and send them to your discord channel through the webhook-url! 



## Docker setup

You can also create a docker image for the bot to run it on a server.

```bash
$ docker image build --platform=linux/amd64 <project_directory> wokobot
$ docker save wokobot:latest | gzip > wokobot.tar.gz
```



