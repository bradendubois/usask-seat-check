# usask-seat-check

A bot to automatically (and repeatedly!) check uSask course availability on Banner, and notify you when a seat is available.

**Disclaimer**: This is an *unofficial* repository that is *unaffiliated* with the University of Saskatchewan.

I made this because it is stressful to check constantly, but also nearly impossible to navigate the new Banner system.

## Requirements

* Python 3
* `pip` or equivalent to install Python libraries
* Discord server for notifications
* Google Chrome for Selenium to navigate Banner
* confidence in writing your actual NSID / password in a text file

## Setup

### Install Requirements

See the [requirements.txt](requirements.txt) file for necessary modules:

```shell
pip install -r requirements.txt
```

You may need additional libraries or software, but the error messages will be relatively informative.

### Create Discord Webhooks

You can use [Discord Webhooks](https://support.discord.com/hc/en-us/articles/228383668-Intro-to-Webhooks) to notify you of the particular state of the course. The script really just `POST`s to whatever webhook is provided, so it could (presumably) notify you through something other than Discord, but this has not been tested.

Three states are defined, each supporting their own webhook:
1. a seat is available
2. no seat is available
3. the bot has encountered an error or unexpected state navigating Banner

Follow [Discord's intro](https://support.discord.com/hc/en-us/articles/228383668-Intro-to-Webhooks) to create your webhooks.
* **Short Version**: `Server Settings` > `Integrations` > `View Webhooks` > `New Webhook`

### Store Search Info

Fill out the [data.json](data.json) file with:
* your student login info (necessary to access Banner)
* the course you want to look for (subject code and number)
* the webhooks and a custom message you want sent with each

## Running

Assuming all prerequisites are fulfilled:

```shell
python3 seat-check.py
```

Selenium will open Chrome and will sign you in. MFA usually is required the first time, so have your authenticator ready. After this, it will repeatedly search for the course, post to the appropriate webhook, and refresh.
