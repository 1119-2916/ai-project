from private.secrets import DISCORD_BOT_TOKEN
import discord
import random


intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print(f"{client.user} has connected to Discord!")


@client.event
async def on_message(message):
    if (
        message.author == client.user
        or message.mention_everyone
    ):
        print(f"{message.author} sent a ignored message: {message.content}")
        return

    random_number = random.randint(1, 100)
    if client.user in message.mentions or random_number < 10:
        print(f"{message.author} sent a action required message: {message.content}")
        await message.channel.send(f"Hello {message.author}!")
    else:
        print(f"{message.author} sent a passed message: {message.content}")


def main():
    client.run(DISCORD_BOT_TOKEN)


if __name__ == "__main__":
    main()
