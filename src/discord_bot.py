import discord
from discord.ext import commands
from dotenv import dotenv_values
from gavin import Gavin
import random
import logging
import asyncio

# Load variables from .env file
env_vars = dotenv_values(".env")
key = env_vars["DISCORD_TOKEN"]

logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s', level=logging.INFO)

intents = discord.Intents.all()
intents.voice_states = True
intents.messages = True 

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.event
async def on_error(event, *args, **kwargs):
    print(f"Error: {event}")

@bot.event
async def on_voice_state_update(member, before, after):
    '''Will do something proper with this later.'''
    print(f"Voice state update: {member} {before} {after}")

@bot.command()
async def join(ctx):
    print("join")
    # Check if the user is in a voice channel
    if ctx.author.voice is not None and ctx.author.voice.channel is not None:
        voice_channel = ctx.author.voice.channel
        # Connect to the voice channel
        await voice_channel.connect()
    else:
        await ctx.send("You are not in a voice channel.")

@bot.command()
async def leave(ctx):
    # Check if the bot is in a voice channel
    if ctx.voice_client is not None:
        # Disconnect from the voice channel
        await ctx.voice_client.disconnect()
    else:
        await ctx.send("I am not in a voice channel.")

@bot.command()
async def stop(ctx):
    """Stops the bot from talking"""
    ctx.voice_client.stop()

@bot.command(name='woe', help='Woe', aliases=['pie','hot'])
async def woe(ctx):
    # Random number 1 in 10 chance of woe
    if random.randint(1, 10) == 1:
        await ctx.send("Hot diggity dog! Woe!")
    else:
        await ctx.send("Woe")

@bot.command(name='say', help='Gavin')
async def say(ctx):
    """text conversation with Gavin"""
    user_message = ctx.message.content[4:].strip()
    print(user_message)
    logging.info(f"[{ctx.author.name}] {user_message}")
    response = gavin.talk_text(user_message)
    await ctx.send(response)

@bot.command( name='talk', help='Gavin speaks to you.', aliases=['play'])
async def talk(ctx):
    """voice conversation with Gavin"""
    if ctx.voice_client is not None and ctx.author.voice is not None:
        user_message = ctx.message.content[5:].strip()
        print(user_message)
        logging.info(f"[{ctx.author.name}] {user_message}")
        response = gavin.talk_text(user_message, True)
        await ctx.send(response)
        audio_file = gavin.talk_audio(response)
        source = discord.FFmpegPCMAudio(audio_file)
        ctx.voice_client.play(source, after=lambda e: print(f'Player error: {e}') if e else None)
    else :
        await ctx.send(f"{ctx.author} not in a voice channel.")

@bot.command(name='paint', help='Gavin paints the conversation.')
async def paint(ctx):
    """paint the conversation"""
    print("Painting the conversation.")
    logging.info("Painting the conversation.")
    message = await ctx.send("Ok I'm making a cool picture, hang on!")
    art_prompt = gavin.paint_conversation()
    art_prompt = "local_image.jpg"
    await message.edit(content = "Here's my art", attachments=[discord.File(art_prompt)])

@bot.command(name='art', help='Gavin paints the prompt.')
async def art(ctx):
    """paint the prompt"""
    message = await ctx.send("Painting the prompt. Hang tight.")
    formatted_user_prompt = ctx.message.content[4:].strip()
    print(formatted_user_prompt)
    logging.info(formatted_user_prompt)
    art_prompt = gavin.paint(formatted_user_prompt)
    await message.edit(content = "Here's your picture", attachments=[discord.File(art_prompt)])

def check_author(ctx):
    match ctx.author.id:
        case ".theejuicetm":
            return True
        case ".lilpage":
            return True
        case"butters4494":
            return True
        case".0blivion":
            return True
        case _:
            return False

# Main initialization
if __name__ == "__main__":
    gavin = Gavin()
    asyncio.run(bot.run(key))
    
    