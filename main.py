import discord
from discord.ext import commands
import asyncio
import os
import logging
from dotenv import load_dotenv


# Import the Bot Token
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

if BOT_TOKEN is None:
    raise ValueError("No BOT_TOKEN found in environment variables")

GUILD_ID = 1302588750630621184

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="/", intents=intents)

# Configure logging to log to a file
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(name)s - %(message)s',
                    filename='bot.log',
                    filemode='w')


@bot.event
async def on_ready():
    """Handles the event that occurs when the Discord bot has successfully connected and is ready."""
    logging.info("Loaded cogs: %s", list(bot.cogs.keys()))
    logging.info(f"We have successfully logged in as {bot.user}")
    logging.info("------------------------------------------------")

    await bot.change_presence(activity=discord.Game(name="/afc_help"))
    print(f"""\nWe have successfully logged in as {
          bot.user}.\n------------------------------------------------""")

    # Sync the command tree for slash commands
    await bot.tree.sync()
    print("Slash commands synced")
    logging.info("Slash commands synced")


async def load_all_extensions():
    """Loads all Python files ending with '.py' in the 'cogs' directory as extensions."""
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            try:
                await bot.load_extension(f"cogs.{filename[:-3]}")
                logging.info(f"Successfully loaded extension: {filename}")
            except Exception as e:
                logging.error(f"Failed to load extension {filename}: {e}")


async def main():
    """Starts the Discord bot by loading all extensions and then running the bot with the given token."""
    async with bot:
        await load_all_extensions()
        await bot.start(BOT_TOKEN)


if __name__ == "__main__":
    asyncio.run(main())
