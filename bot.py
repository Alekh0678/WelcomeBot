import discord
from discord.ext import commands
import os
import logging

# Set up logging for production readiness and error tracking
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class WelcomeBot(commands.Bot):
    def __init__(self):
        # Enable necessary intents
        intents = discord.Intents.default()
        intents.members = True
        intents.message_content = True
        
        # Initialize the bot
        super().__init__(command_prefix="!", intents=intents)

    async def on_ready(self):
        logging.info(f'Bot is online! Logged in as {self.user} (ID: {self.user.id})')
        logging.info('Ready to welcome new members.')
        print('------')

    async def on_member_join(self, member):
        # Attempt to find a channel named 'general'
        channel = discord.utils.get(member.guild.text_channels, name='welcome')
        
        # Fallback to the server's default system channel if 'general' is not found
        if channel is None:
            channel = member.guild.system_channel

        if channel is not None:
            try:
                # Create the beautiful green welcome embed
                embed = discord.Embed(
                    title="🎉 Welcome to the Server! 🎉",
                    description=f"Namaste aur swagat hai {member.mention} hamare server **{member.guild.name}** mein! Aasha hai aap yahan bahut enjoy karenge.",
                    color=discord.Color.green()
                )
                
                # Set user profile picture as thumbnail
                if member.display_avatar:
                    embed.set_thumbnail(url=member.display_avatar.url)
                
                # Show total member count
                embed.add_field(
                    name="Member Count", 
                    value=f"Aap hamare **{member.guild.member_count}th** member hain! 🥳", 
                    inline=False
                )
                
                embed.set_footer(text="Have a great time interacting with everyone!")

                # Send the embed to the channel
                await channel.send(embed=embed)
                
            except discord.Forbidden:
                logging.error(f"Error: Missing permissions to send messages or embeds in #{channel.name} for guild '{member.guild.name}'.")
            except discord.HTTPException as e:
                logging.error(f"HTTP Exception while sending welcome message: {e}")
            except Exception as e:
                logging.error(f"An unexpected error occurred: {e}")
        else:
            logging.warning(f"Could not find a 'general' or system channel in '{member.guild.name}' to send the welcome message.")

if __name__ == "__main__":
    # Securely load the token from environment variables
    token = os.getenv("DISCORD_TOKEN")
    
    if not token:
        logging.critical("DISCORD_TOKEN environment variable is not set. Please configure it before hosting.")
    else:
        bot = WelcomeBot()
        bot.run(token)