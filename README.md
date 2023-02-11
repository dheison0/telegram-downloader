[Pyrogram Framework]: <https://github.com/pyrogram/pyrogram>
[My Telegram]: <https://my.telegram.org>
[BotFather]: <https://t.me/BotFather>


# Telegram downloader

This is a *simple* bot to download telegram files directly to your own server
without needing to keep telegram open or using telegram-cli, this uses Telegram's
MTProto protocol to download files up to 4GB using the [Pyrogram Framework].

## Setup

To setup this bot on your own server you'll need a Telegram API ID/Hash, it can be
created at [My Telegram] website, do this before continue

If you want to run this bot on a docker server follow [Environment variables](#Environment%20variables)
guide and then [Docker install](#Docker%20install) guide.

## Install dependencies

To install all needed dependencies use pip:

```bash
python3 -m pip install -r requirements.txt
```

If you have any issue, try to install build-essentials in your system, the `psutil`
lib sometimes needs to be builded locally.

## Environment variables

Observation: *This bot support dot files(`.env`)*

Now that you've your own ID/Hash it has be passed to `TELEGRAM_API_ID` and
`TELEGRAM_API_HASH` environment variables, you also need to set the bot token(create
one [here][BotFather]) as `BOT_TOKEN`

The default download folder is `/data`, if you want to set another location define that
as `DOWNLOAD_FOLDER`

You also need to set the bot administrator list using `ADMINS`, use spaces to separate
everyone.

## Running

To run this bot it has to be started as a module, to this use `-m` flag:

```bash
python3 -m bot
```

When you wanna stop the bot, press CTRL+\\

## Docker run

This bot is so simple that you only need to set some environment variables and mount a
folder inside the container to keep your downloads, for this, use this command replacing
values with your owns:

```bash
# Build a docker image to your own server
docker build -t telegram-downloader .

# Now run this
docker run -d \
    -v /home/$USER/Telegram:/data \
    -e TELEGRAM_API_ID=123456 \
    -e TELEGRAM_API_HASH="yourTelegramAPIHash" \
    -e BOT_TOKEN="yourBotToken" \
    -e ADMINS="@yourTelegramUsername" \
    telegram-downloader
```
