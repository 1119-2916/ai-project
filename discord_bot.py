from private.secrets import DISCORD_BOT_TOKEN
from logging import getLogger, INFO, DEBUG
import logging
import discord
import random
import json


# ロガーの設定
logging.basicConfig(level=INFO)

logger = getLogger(__name__)
logger.setLevel(DEBUG)


intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)


@client.event
async def on_ready():
    logger.info(f"{client.user} has connected to Discord!")


@client.event
async def on_message(message):
    if (
        message.author == client.user
        or message.mention_everyone
    ):
        logger.info(f"{message.author} sent a ignored message: {message.content}")
        return

    random_number = random.randint(1, 100)
    if client.user in message.mentions or random_number < 10:
        logger.info(f"{message.author} sent a action required message: {message.content}")
        await message.channel.send(f"Hello {message.author}!")
    else:
        logger.info(f"{message.author} sent a passed message: {message.content}")


# 全てのテキストチャンネルに投稿されたメッセージを収拾する
async def crawl():
    for channel in client.get_all_channels():
        logger.info(f"Channel: {channel.name}")
        result: list[tuple[str, str]] = []
        if channel.type == discord.ChannelType.text:
            logger.info(f"TextChannel: {channel.name}")
            async for message in channel.history(limit=None):
                result.append((message.author.name, message.content))
            with open(f"./chat_log/{channel.name}.txt", "w") as f:
                json.dump(result, f, ensure_ascii=False)


def main():
    client.run(DISCORD_BOT_TOKEN)


if __name__ == "__main__":
    main()
