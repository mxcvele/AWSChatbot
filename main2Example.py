# Import the discord.py library, allowing access to Discord's API.
import discord

# Create an instance of the Client, synonymous with a bot in Discord.
bot = discord.Client()

# Event listener triggered when the bot transitions from offline to online.
@bot.event
async def on_ready():
    # Counter to keep track of the number of guilds/servers the bot is connected to.
	guild_count = 0

    # Iterate through all the guilds/servers the bot is associated with.
	for guild in bot.guilds:
        # Print each server's ID and name.
		print(f"- {guild.id} (name: {guild.name})")

        # Increment the guild counter.
		guild_count = guild_count + 1

    # Display the total number of guilds/servers the bot is in.
	print("SampleDiscordBot is in " + str(guild_count) + " guilds.")

# Event listener triggered when a new message is sent to a channel.
@bot.event
async def on_message(message):
    # Check if the received message is exactly "hello".
	if message.content == "hello":
        # Send a response message to the channel.
		await message.channel.send("hey dirtbag")

# Execute the bot with the specified token (token used here is an example).
bot.run("token")