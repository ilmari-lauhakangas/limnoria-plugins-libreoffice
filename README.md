These are plugins for [Limnoria](https://limnoria.net/), a Python IRC bot. They are used on LibreOffice channels.

QuitAlert monitors one or more nicknames (typically bots) and alerts people, if they disconnect.

Welcome is a reimplementation of [WelcomeBot](https://github.com/qarkai/WelcomeBot/tree/Py3), which was originally used by OpenHatch. The idea is to welcome newcomers, but in a way that minimises noise on the channel. The bot has a wait period and if people talk in the channel during the wait, it will not say anything.

## Setup

1. Install Limnoria, preferably from the [package repository of your Linux distribution](https://repology.org/project/limnoria/versions)
2. Create a directory for the bot and in it a directory called `plugins`
3. Copy the plugin directories into the `plugins` directory
4. In the bot directory, run `supybot-wizard`
5. Say yes to the question about being an advanced user as it will allow you to configure the plugins as well
6. Add yourself as the owner of the bot and store the password into your password manager
7. Say no to the question about sharing the plugin databases by all channels
8. Run the bot with `supybot nameofbot.conf`

The greeters (people to be alerted of newcomers) for Welcome are channel-specific and are configured separately.

1. When your bot is running and connected, identify yourself by saying `/query nameofbot identify myname my password`
2. Now you can configure the bot by saying to it in a channel `nameofbot: config channel #somechannel plugins.Welcome.greeters somenick someothernick` (or addressing it with `@config`, if you chose to use a prefix in the wizard)

The settings that are not channel-specific can be changed in this way: `nameofbot: config plugins.Welcome.waitPeriod 60`.

The Welcome plugin stores known nicks in the SQLite3 database file `data/global/Welcome.sqlite3.db`. If a newcomer disconnects during the wait period, their nick is not stored. If a newcomer changes their nick (even multiple times) during the wait period, the most recent nick is stored. The nicks are cleaned before storing, so typical appended extra stuff such as numbers are left out.

If you want to import nicks, an easy way is to create a CSV file with ID numbers as the first column and the nicks as the second. Then,

1. `sqlite3 Welcome.sqlite3.db`
2. `.import --csv /path/to/nicks.csv nicks`
3. `.quit`

[DB Browser for SQLite](https://sqlitebrowser.org/) is one handy way to quickly inspect the nick database.
