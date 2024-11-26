import discord
from discord import app_commands
from discord.ext import commands


class Admin(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    async def create_embed(self, interaction: discord.Interaction):
        embed_response = discord.Embed(color=discord.Color.blue())

        def _check(m):
            return m.author == interaction.user and m.channel == interaction.channel
        
        try:
            embed_response.title = "Embed Creation"
            embed_response.description = "Please enter a header: (You can type the responses in chat and I'll do the rest 😁)"
            await interaction.response.send_message(embed=embed_response, ephemeral=True)

            header_msg = await self.bot.wait_for('message', check=_check, timeout=600)
            header = header_msg.content

            embed_response.description = "Please enter a body:"
            await interaction.followup.send(embed=embed_response, ephemeral=True)
            body_msg = await self.bot.wait_for('message', check=_check, timeout=600)
            body = body_msg.content

            embed_response.description = "Please enter a hex color (e.g., #ff5733) or type 'none' for default:"
            await interaction.followup.send(embed=embed_response, ephemeral=True)
            color_msg = await self.bot.wait_for('message', check=_check, timeout=300)
            color_content = color_msg.content.lower()
            if color_content == "none":
                color = discord.Color.blue()
            else:
                try:
                    color = discord.Color(int(color_content.lstrip('#'), 16))
                except ValueError:
                    embed_response.description = "Invalid hex color. Using default color."
                    await interaction.followup.send(embed=embed_response, ephemeral=True)
                    color = discord.Color.blue()

            embed_response.description = "Do you want to add a thumbnail? 'yes' or 'no':"
            await interaction.followup.send(embed=embed_response, ephemeral=True)
            answer_msg = await self.bot.wait_for('message', check=_check, timeout=300)
            answer = answer_msg.content.lower()

            url = ""
            if answer == "yes":
                embed_response.description = "Please provide me with an image address URL."
                await interaction.followup.send(embed=embed_response, ephemeral=True)
                thumbnail_url = await self.bot.wait_for("message", check=_check, timeout=600)
                url = thumbnail_url.content

                # Validate the URL
                if not url.startswith(("http://", "https://")):
                    embed_response.description = "Invalid URL. Please ensure it starts with 'http://' or 'https://'."
                    await interaction.followup.send(embed=embed_response, ephemeral=True)
                    return None

            embed = discord.Embed(title=header, description=body, color=color)
            if url:
                embed.set_thumbnail(url=url)

            embed_response.description = "Do you want to add fields to the embed? 'yes' or 'no':"
            await interaction.followup.send(embed=embed_response, ephemeral=True)
            fields_answer_msg = await self.bot.wait_for('message', check=_check, timeout=300)
            fields_answer = fields_answer_msg.content.lower()

            while fields_answer == "yes":
                embed_response.description = "Please enter the field name:"
                await interaction.followup.send(embed=embed_response, ephemeral=True)
                field_name_msg = await self.bot.wait_for('message', check=_check, timeout=300)
                field_name = field_name_msg.content

                embed_response.description = "Please enter the field value:"
                await interaction.followup.send(embed=embed_response, ephemeral=True)
                field_value_msg = await self.bot.wait_for('message', check=_check, timeout=300)
                field_value = field_value_msg.content

                embed_response.description = "Should this field be inline? 'yes' or 'no':"
                await interaction.followup.send(embed=embed_response, ephemeral=True)
                field_inline_msg = await self.bot.wait_for('message', check=_check, timeout=300)
                field_inline = field_inline_msg.content.lower() == "yes"

                embed.add_field(name=field_name, value=field_value, inline=field_inline)

                embed_response.description = "Do you want to add another field? 'yes' or 'no':"
                await interaction.followup.send(embed=embed_response, ephemeral=True)
                fields_answer_msg = await self.bot.wait_for('message', check=_check, timeout=300)
                fields_answer = fields_answer_msg.content.lower()

            bot_user = self.bot.user
            embed.set_footer(
                text=f"{bot_user.name}", icon_url=bot_user.avatar.url if bot_user.avatar else None)
            return embed
        except Exception as e:
            embed_response.description = f"An error occurred: {str(e)}"
            await interaction.followup.send(embed=embed_response, ephemeral=True)
            return None
        

    @app_commands.command(name="announce", description="Post an embedded message to a server channel")
    @app_commands.checks.has_permissions(kick_members=True)
    async def announce(self, interaction: discord.Interaction, channel: discord.TextChannel):
        embed = await self.create_embed(interaction)
        if embed:
            await channel.send(embed=embed)
            await interaction.followup.send("Messages successfully posted!", ephemeral=True)

    @announce.error
    async def announce_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.CheckFailure):
            await interaction.response.send_message("You don't have permission to post announcements!", ephemeral=True)
        else:
            await interaction.response.send_message(f"An error occurred: {str(error)}", ephemeral=True)



async def setup(bot):
    await bot.add_cog(Admin(bot))
