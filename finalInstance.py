# Run the bot with the retrieved token
# Import neccessary libraries
import discord
import os
import random 
from ec2_metadata import ec2_metadata 

# Retrieve EC2 instance metadata
instance_id = ec2_metadata.instance_id
region = ec2_metadata.region
availability_zone = ec2_metadata.availability_zone
public_ipv4 = ec2_metadata.public_ipv4
private_ipv4 = ec2_metadata.private_ipv4

# Display EC2 instance metadata
print(ec2_metadata.region)
print(ec2_metadata.instance_id)
print(f"Instance ID: {instance_id}")
print(f"Region: {region}")
print(f"Availability Zone: {availability_zone}")
print(f"Public IPv4: {public_ipv4}")
print(f"Private IPv4: {private_ipv4}")

# Discord client initialization 
client = discord.Client()

# Retrieve the bot token from the environment variable
token = os.getenv('TOKEN')

# Check if the token was retrieved successfully
if token:
    print("Token retrieved successfully:", token)
else:
    print("TOKEN environment variable not found.")

# Event : Bot is ready     
@client.event
async def on_ready():
    print(f"Logged in as a bot {client.user}")

# Event: Message recieved
@client.event
async def on_message(message):
    username = str(message.author).split("#")[0]
    channel = str(message.channel.name)
    user_message = str(message.content)
    
    print(f'Message {user_message} by {username} on {channel}')
    
    if message.author == client.user:
        return
    
    try:
        # Check if the message is in the "random" channel
        if channel == "random":
            # Bot response based on user input
            if user_message.lower() == "boomer?" or user_message.lower() == "boomer?":
                await message.channel.send(f"Sooner! {username} Your EC2 Data: {ec2_metadata.region}")
                return
            
            elif user_message.lower() == "hello?":
                await message.channel.send(f'Sooner! {username}')
            
            elif user_message.lower() == "ec2 data":
                await message.channel.send("Your instance data is " + ec2_metadata.region)

            if user_message.lower() == "tell me about my server!":  # Check for specific message
                # Provide details about the EC2 server
                ip_address = ec2_metadata.private_ipv4  # Assuming you want the private IP, change if needed
                response = f"IP Address: {ip_address}\nAWS Region: {ec2_metadata.region}\nAvailability Zone: {ec2_metadata.availability_zone}"
                await message.channel.send(response)

            # Bot responds to the phrase "greetings"
            elif "greetings" in user_message.lower():
                await message.channel.send(f'Greetings, {username}!')
            
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


# Run the bot with the retrieved token
client.run(token)