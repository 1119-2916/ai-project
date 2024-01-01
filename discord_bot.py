from private.secrets import DISCORD_BOT_TOKEN, VC_CHANNEL_DICT, BOT_ID
from logging import getLogger, INFO, DEBUG
from kurobara_ai import KurobaraAI
from urlextract import URLExtract
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

kurobara_ai = KurobaraAI()
url_extractor = URLExtract()


@client.event
async def on_ready():
    logger.info(f"{client.user} has connected to Discord!")


@client.event
async def on_message(message):
    # 返事をしない場合は何もしない
    rate: int = VC_CHANNEL_DICT.get(str(message.channel.id), 40)
    if not _is_reply(message, rate):
        return

    # メンションであった場合、メンション文字列が混ざるのでこれは削除する
    chat_text: str = message.content.replace(BOT_ID, "")

    # メッセージに画像が含まれる場合
    if len(message.attachments) > 0:
        # メンションでなければ無視
        if not client.user in message.mentions:
            return
        content_type: str = message.attachments[0].content_type
        if content_type.startswith("image"):
            logger.info(f"{message.author} sent a image: {message.attachments[0].url}")
            logger.info(f"reply to {chat_text}")
            await message.channel.send(kurobara_ai.generate_reply_to_including_image(chat_text))
            return
        else:
            # 画像以外は無視
            logger.info(f"{message.author} sent a {content_type}")
            return

    # メッセージにURLが含まれる場合
    urls: list[str] = url_extractor.find_urls(chat_text)
    if len(urls) > 0:
        # メンションでなければ無視
        if not client.user in message.mentions:
            return
        logger.info(f"{message.author} sent a URL: {urls[0]}")
        for url in urls:
            chat_text = chat_text.replace(url, "")
        logger.info(f"reply to {chat_text}")
        await message.channel.send(kurobara_ai.generate_reply_to_including_URL(chat_text))
        return

    # 返事をする
    reply = kurobara_ai.generate_reply(chat_text)
    logger.info(f"{message.author} sent a message: {chat_text}, response: {reply}")

    if len(reply) == 0:
        return
    await message.channel.send(reply)


# 返事をするか判断する
def _is_reply(message, rate: int = 40) -> bool:
    # 自分自身の投稿と、@everyoneへのメンションは無視する
    if (
        message.author == client.user
        or message.mention_everyone
    ):
        return False

    # メンションには絶対に反応する
    if client.user in message.mentions:
        return True

    # 40% の確率で返事をする
    return random.randint(1, 100) < rate


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
