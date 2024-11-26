import discord
import logging
from discord.ext import commands, tasks
from datetime import datetime, timedelta
import schedules
from main import GUILD_ID  # Import GUILD_ID from main.py

class EventNotifier(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.event_notification_task.start()
        logging.info("EventNotifier task has started.")

    async def cog_unload(self):
        self.event_notification_task.cancel()

    @tasks.loop(minutes=1)
    async def event_notification_task(self):
        now = datetime.now()
        logging.info(f"Checking events at {now}")

        # Loop through the test event
        for event in schedules.RUBBING_ADINHOS_BELLY:
            event_day = str(event["day"])
            event_hour = int(event["hour"])
            event_minute = int(event.get("minute", 0))
            role_id = event["role_id"]

            logging.info(f"Processing test event scheduled for {event_day} at {event_hour}:{event_minute}")

            # Calculate event time
            days_until_event = (
                ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"].index(event_day)
                - now.weekday() + 7
            ) % 7
            event_time = now + timedelta(days=days_until_event)
            event_time = event_time.replace(hour=event_hour, minute=event_minute, second=0, microsecond=0)

            time_difference = event_time - now
            logging.info(f"Time difference for test event: {time_difference}")

            # Adjusted condition to include <= timedelta(0)
            if timedelta(minutes=0) <= time_difference <= timedelta(minutes=1):
                logging.info(f"Triggering notification for test event.")
                await self.send_notification(role_id, "Rubbing Adinho's Belly", event_time, "1 minute")
        
    async def send_notification(self, role_id, event_name, event_time, time_remaining):
        CHANNEL_ID = 1306750460153036880  # Replace with your channel ID

        guild = self.bot.get_guild(GUILD_ID)  # Fetch the guild using GUILD_ID
        if guild is None:
            logging.error(f"Guild with ID {GUILD_ID} not found")
            return

        role = discord.utils.get(guild.roles, id=role_id)
        channel = guild.get_channel(CHANNEL_ID)  # Fetch the specific channel by ID

        if role and channel:
            unix_timestamp = int(event_time.timestamp())
            await channel.send(
                f"{role.mention} Reminder: {event_name} starts in {time_remaining}! \nScheduled for <t:{unix_timestamp}:F> (<t:{unix_timestamp}:R>)."
            )
        else:
            if not role:
                logging.error(f"Role with ID {role_id} not found in guild {guild.name}")
            if not channel:
                logging.error(f"Channel with ID {CHANNEL_ID} not found in guild {guild.name}")

    @event_notification_task.before_loop
    async def before_event_notification_task(self):
        await self.bot.wait_until_ready()

async def setup(bot):
    await bot.add_cog(EventNotifier(bot))