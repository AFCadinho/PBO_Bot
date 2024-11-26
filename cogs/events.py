import discord
import schedules

from discord import app_commands
from discord.ext import commands
from datetime import datetime, timedelta


class Events(commands.Cog):

    def __init__(self, bot) -> None:
        self.bot = bot

    # Autocomplete function for event_type
    async def event_type_autocomplete(self, interaction: discord.Interaction, current: str) -> list[app_commands.Choice[str]]:
        event_types = ["crew_wars", "bug_catching", "fishing", "dynamax"]
        return [
            app_commands.Choice(name=event, value=event)
            for event in event_types
            if current.lower() in event.lower()
        ]

    @app_commands.command(name="event_schedule", description="Shows the next event of the specified type.")
    @app_commands.autocomplete(event_type=event_type_autocomplete)
    async def event_schedule(self, interaction: discord.Interaction, event_type: str):
        """Displays the next event for the specified type."""
        try:
            # Determine the schedule based on event type
            if event_type.lower() == "bug_catching":
                schedule = schedules.BUG_CATCHING_SCHEDULE
                event_name = "Bug Catching Competition"
            elif event_type.lower() == "fishing":
                schedule = schedules.FISHING_COMPETITION_SCHEDULE
                event_name = "Fishing Competition"
            elif event_type.lower() == "dynamax":
                schedule = schedules.DYNAMAX_INVASION_SCHEDULE
                event_name = "Dynamax Invasion"
            elif event_type.lower() == "crew_wars":
                schedule = schedules.CREW_WARS_SCHEDULE
                event_name = "Crew Wars"
            else:
                await interaction.response.send_message("Invalid event type. Choose from: bug_catching, fishing, dynamax.", ephemeral=True)
                return

            now = datetime.now()
            nearest_event = None
            min_time_difference = timedelta.max

            # Calculate the datetime for each event and find the nearest one
            for event in schedule:
                event_day = str(event["day"])
                event_hour = int(event["hour"])

                # Calculate the next occurrence of the event
                days_until_event = (
                    ["Monday", "Tuesday", "Wednesday", "Thursday",
                        "Friday", "Saturday", "Sunday"].index(event_day)
                    - now.weekday() + 7
                ) % 7
                event_time = now + timedelta(days=days_until_event)
                event_time = event_time.replace(
                    hour=event_hour, minute=0, second=0, microsecond=0)

                # Check if this event is the nearest
                time_difference = event_time - now
                if timedelta(0) < time_difference < min_time_difference:
                    nearest_event = {"day": event_day, "time": event_time}
                    min_time_difference = time_difference

            # If no future event is found (unlikely), handle gracefully
            if not nearest_event:
                await interaction.response.send_message(f"No upcoming {event_name} events found.", ephemeral=True)
                return

            # Format the nearest event
            event_day = nearest_event["day"]
            event_time = nearest_event["time"]

            # Convert to Unix timestamp
            if isinstance(event_time, datetime):
                unix_timestamp = int(event_time.timestamp())
            else:
                raise TypeError(f"""Expected datetime object, got {
                                type(event_time)} instead""")

            # Create the embed
            embed = discord.Embed(
                title=f"Next {event_name}",
                description=f"The next {event_name} event is:",
                color=discord.Color.gold(),
            )
            embed.add_field(
                name=f"{event_day}",
                value=f"<t:{unix_timestamp}:F> - (<t:{unix_timestamp}:R>)",
                inline=False,
            )
            embed.set_footer(
                text="All times are automatically adjusted to your local timezone.")

            # Send the response
            await interaction.response.send_message(embed=embed)

        except Exception as e:
            await interaction.response.send_message(f"An error occurred: {str(e)}", ephemeral=True)


async def setup(bot):
    await bot.add_cog(Events(bot))
