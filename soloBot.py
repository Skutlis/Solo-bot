import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import os 
import random
import time
import numpy as np
import m


load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')

GUILD = os.getenv('DISCORD_GUILD')

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix=';')


print('Solo-Bot Ready!')


@bot.command(name = 'split')
async def _split(ctx, size = 2):
    solobotID = 938116538878296064
    channel = bot.get_channel(solobotID)

    sender = ctx.author
    voice_channel = sender.voice.channel
    if voice_channel:
        membersID = voice_channel.voice_states.keys()
        members = []
        
        
        for id in membersID:
            nxt = await ctx.message.guild.query_members(user_ids=[id])
            if not nxt[0].nick == None:
                members.append(nxt[0].nick)
        
        

        np.random.shuffle(members)
        team = 1
        msg = f'Team {team}: '
        for i in range(len(members)):
            if i % size == 0 and i != 0:
                team += 1
                msg += '\n' + f'Team {team}: '
            msg += members[i] 
            
            if (i+1) < len(members) and (i+1) % size != 0:
                msg += ' - '

        await channel.send(msg)


@bot.command(name = 'coinflip')
async def _coinflip(ctx, choose = 'tails'): 
    solobotID = 938116538878296064
    channel = bot.get_channel(solobotID)
    rand = random.randint(0, 1)
    if rand == 0:
        msg = 'tails'
    else:
        msg = 'heads'
    await channel.send(msg)
    
            

@bot.command(name = 'join', help = 'Tells the bot to join the voice channel')
async def join(ctx):
    if not ctx.message.author.voice:
        await ctx.send(f'{ctx.message.author.name} is not connected to a voice channel')
        return
    else:
        channel = ctx.message.author.voice.channel

    await channel.connect()

@bot.command(name= 'leave', help = 'To make the bot leave the voice channel')
async def leave(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_connected():
        await voice_client.disconnect()
    else:
        await ctx.send("The bot is not connected to a voice channel.")


@bot.command(name = 'play', help = 'To play song')
async def play(ctx, url):
    if url == '':
        await ctx.send('URL to youtube video needed!')
        return
    try :
        server = ctx.message.guild
        voice_channel = server.voice_client
        

        async with ctx.typing():
            filename = await m.YTDLSource.from_url(url, loop = bot.loop)
            voice_channel.play(discord.FFmpegPCMAudio(executable = 'ffmpeg.exe', source = filename))
           

        await ctx.send(f'**Now playing: ** {filename}') 
    
    except:
        await ctx.send('The bot is not connected to a voice channel.')


@bot.command(name = 'pause', help = 'This command pauses the song')
async def pause(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_playing():
        await voice_client.pause()
    else:
        await ctx.send('The bot is not playing anything at the moment')

@bot.command(name = 'resume', help = 'Resumes the song')
async def resume(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_paused():
        await voice_client.resume()
    else:
        await ctx.send('The bot was not playing anything before this. Use play command')


@bot.command(name = 'stop', help = 'Stops the song')
async def stop(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_playing():
        await voice_client.stop()
    else:
        await ctx.send('The bot is not playing anything at the moment.')

"""
if __name__ == '__main__':
    bot.run(TOKEN)
"""
bot.run(TOKEN)

