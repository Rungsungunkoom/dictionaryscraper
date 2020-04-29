# Word of the Day Discord bot
This repo contains code that enables a Word of the Day Discord bot. How it works is that it web scrapes all works from [dictionary.com](https://dictionary.com) into a SQLite database and exposes a set of commands to generate query random words and calls a webhook for sending your guild a random word every day.

## Getting started
1. To get started, you need to have python3 installed. And you must also have the following packages installed via pip:

- sqlite3
- pathlib
- requests
- bs4
- discord_argparse
- discord
- json
- asyncio

2. You need to create dictionary.db, so run dictionary_scraping/dictionary_scrape.py to scrape all words and save them into *.csv and *.sql files. These files will be written to the home directory (C:\\Users\\<username> for Windows and ~ for \*nix)

3. After you have all the \*.sql files (\*.csv files aren't really used), then it's time to crate the SQLite database (dictionary.db) in the home directory. To this, run create_database.py

4. Now you need to create a Discord bot, you can Google that, set the following environment variables accordingly:
- DISCORD_GUILD
- DISCORD_TOKEN
- DISCORD_WEBHOOK

5. Run wordquery.py directly to use the webhook created to send a word to your guild's channel.

6. Run woddiscordbot.py to connect your Discord bot to your guild.

You can run the BOT in whatever way you wish, but a simply solution is to set a crontab for running the wordquery.py script daily and a systemd service to run the bot.