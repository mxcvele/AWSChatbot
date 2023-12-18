import discord
import os
import random
from ec2_metadata import ec2_metadata
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Discord client
client = discord.Client()
DEVELOPMENT_ENV = os.getenv('DEVELOPMENT_ENV') == 'True'
token = os.getenv('TOKEN') if DEVELOPMENT_ENV else os.getenv('PRODUCTION_TOKEN')

# Event-driven function when the client connects to Discord
@client.event
async def on_ready():
    print("Logged in as a bot {0.user}".format(client))

# Event-driven function triggered when a message is received
@client.event
async def on_message(message):
    # Extract nessage details
    username = str(message.author).split("#")[0]
    channel = str(message.channel.name)
    user_message = str(message.content)
    
    print(f'Message {user_message} by {username} on {channel}')
    
    if message.author == client.user:
        return
    
    try:
          # Check if the message is in the "random" channel
        if channel == "random":
             # Bot responses based on user input
            if user_message.lower() == "boomer?" or user_message.lower() == "boomer?":
                await message.channel.send(f"Sooner! {username} Your EC2 Data: {ec2_metadata.region}")
                return
            
            elif user_message.lower() == "hello?":
                await message.channel.send(f'Sooner! {username}')
            
            elif user_message.lower() == "ec2 data":
                await message.channel.send("Your instance data is " + ec2_metadata.region)
            
            elif user_message.lower() == "tell me about my server!":
                # Provide details about the EC2 server
                ip_address = ec2_metadata.private_ipv4 if DEVELOPMENT_ENV else ec2_metadata.public_ipv4
                response = f"IP Address: {ip_address}\nAWS Region: {ec2_metadata.region}\nAvailability Zone: {ec2_metadata.availability_zone}"
                await message.channel.send(response)
            
            # Additional commands
            elif user_message.lower() == "info":
                await message.channel.send("This is a Discord bot running on an AWS EC2 instance.")
            
            # Add more commands here
        
    # Error handling for Discord API issues
    except discord.errors.HTTPException as discord_error:
        print(f"Discord API Error: {discord_error}")
        await message.channel.send("Error accessing Discord API. Please try again later.")

    # Error handling for EC2 Metadata access issues
    except ec2_metadata.NotAvailableError as ec2_error:
        print(f"EC2 Metadata Error: {ec2_error}")
        await message.channel.send("Error accessing EC2 Metadata. Please try again later.")
    
    # General error handling
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        await message.channel.send("An unexpected error occurred. Please try again later.")

# Start the bot by passing the token
client.run('TOKEN')