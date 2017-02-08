# Raspberry Pi Monitor

This project is meant to record some statistics about your raspberry pi (with some type of linux running) in a [Firebase](https://firebase.google.com/) database. You can use this to keep track of information like temperature, disk usage, IP address, and more.

If you are interested in temperature specifically, you should also check out my  [pi-temperature-firebase](https://github.com/mrnohr/pi-temperature-firebase) project to track the temperature of your raspberry pi over time.

While this was initially intended to only work on a raspberry pi, it is possible that it could work on any linux-based system. I have tried it on a Apple computer, which mostly worked.

## Installation

### Scripts

You will need to copy the script to your pi. One easy way would be to just clone this repo.

### Config

You will need to copy the `config.json.example` to your home directory (`~/`), rename it to `config.json`, and fill in your specific information.

### Cron Scheduling

You also need to set up the scripts to run on a regular basis. To do this, you should use `crontab`.

1. On the pi, enter `crontab -e`
2. Use the following cron settings, or adjust to report as frequently as you want.

```
*/10 * * * * python /home/pi/pi-monitor-firebase/getStats.py
```

Make sure the paths defined point to your scripts.

## Firebase

To use this you will need to setup a Firebase project. In the code the `pi-temperature-c369d` is a sample project I used for testing.

### Firebase Auth

You will need a database secret to use as `auth`. Note that the `ItdM8YVCzL5YBbiEM2sSax92JhficBxvFPPKBzXz` value I have throughout the code is a revoked auth secret I used for testing.

Under [Gear] > Project Settings > Service Accounts > Database Secrets

### Firebase Rules

I just used the default rules.

Under Database > Rules:

```
{
  "rules": {
    ".read": "auth != null",
    ".write": "auth != null"
  }
}
```

## Python Dependencies

### pip

This isn't strictly required, but it is the easiest way to get the `requests` python package. More information on `pip` can be found here: [website](https://pip.pypa.io/en/stable/)

To install `pip` on the raspberry pi:

1. `wget https://bootstrap.pypa.io/get-pip.py`
2. `sudo python get-pip.py`

### requests library
The `requests` python package is used to make the REST API calls to Firebase. More information can be found here: [website](http://docs.python-requests.org/en/master/)

Assuming you have `pip` installed, all you need to do is:

1. `sudo pip install requests`

## Next Steps

- [ ] Make config file be somewhere other than ~/
