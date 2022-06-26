from code import interact
from pickle import PickleBuffer
import discord
import os
import asyncio
import youtube_dl
from discord.ext import commands
from discord import Embed, Role
from discord import guild
from discord import member
from discord.ui import Button
from discord.ui import View
import random

token = "OTg1MTE0MTQ4Njc1Mzg3NDAy.Goqmc4.TPdDaKOfrIO2DRNJL782Xg4JuyzcSOhHfltmaY"
prefix = "j!"
blocked_words = ["fuck", "shit", "pis", "lort", "homo", "bitch", "nigga", "nigger", "neger", "pik", "diller"]

voice_clients = {}

yt_dl_opts = {'format': 'bestaudio/best'}
ytdl = youtube_dl.YoutubeDL(yt_dl_opts)

ffmpeg_options = {'options': "-vn"}

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True
intents.members = True

client = commands.Bot(command_prefix="j!", intents=intents)



@client.event
async def on_ready():
    print(f"Bot logged in as {client.user}")

@client.event
async def on_message(msg):
    if msg.author != client.user:
        if msg.content.lower().startswith(f"{prefix}info"):
            await msg.channel.send(f"Hi, Im JoksysBot Made By Joksy! Type `j!commands_help` for a list of commands to use!")
        if msg.content.lower().startswith(f"{prefix}commands_help"):
            await msg.channel.send(f"These are the commands you can use: `j!info`. Give info, `j!commands_help`. Gives help, `j!play (youtube url here) `. Plays sound from a youtube video, `j!pause`. Pauses the audio from a youtube video, `j!resume`. Resumes the audio from a youtube video after a pause, `j!stop`. Stops the audio from a youtube video and leaves the voice call. `j!gandpreact`. Sends role buttons (need Admin role to use this command)")

        if msg.content.lower().startswith(f"{prefix}gandpreact"):
            if "Admin" in str(msg.author.roles):
                
                guild = msg.guild
            
                programmer_role = discord.utils.get(guild.roles, name="Programmer")
                gamer_role = discord.utils.get(guild.roles, name="Gamer")

                async def pbutton_callback(interaction):
                    await interaction.response.send_message("Added Programmer role!", ephemeral=True)
                    user = interaction.user
                    await user.add_roles(programmer_role)
                
                
                async def gbutton_callback(interaction):
                    await interaction.response.send_message("Added Gamer role!", ephemeral=True)
                    user = interaction.user
                    await user.add_roles(gamer_role)

                programmer_button = Button(label="Click me for Programmer role!", style=discord.ButtonStyle.blurple)
                programmer_button.callback = pbutton_callback

                gamer_button = Button(label="Click me for Gamer role!", style=discord.ButtonStyle.red)
                gamer_button.callback = gbutton_callback

                view = View()
                view.add_item(programmer_button)
                view.add_item(gamer_button)

                await msg.channel.send("Click the button for a role", view=view)
            elif "Admin" not in str(msg.author.roles):
                await msg.channel.send("You need Admin role to use that command!")
        if msg.content.lower().startswith(f"{prefix}social_media"):
            yt_button = Button(label="Go To Youtube Channel", style=discord.ButtonStyle.red, url="https://www.youtube.com/channel/UCyGn4cwoAsKYzDUuTdhJZdw")
            twitter_button = Button(label="Go To Twitter Profile", style=discord.ButtonStyle.blurple, url="https://twitter.com/Joksys")
            ttv_button = Button(label="Go To Twitch Channel", url="https://www.twitch.tv/joksyyt")

            view = View()

            view.add_item(yt_button)
            view.add_item(twitter_button)
            view.add_item(ttv_button)

            await msg.channel.send(view=view)

        for text in blocked_words:
            if text in str(msg.content.lower()):
                await msg.delete()
                await msg.channel.send("Hey, Dont Say That!")
                return
        if msg.content.startswith(f"{prefix}play"):

            
            voice_client = await msg.author.voice.channel.connect()
            voice_clients[voice_client.guild.id] = voice_client

            url = msg.content.split()[1]

            loop = asyncio.get_event_loop()
            data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=False))

            song = data['url']
            player = discord.FFmpegPCMAudio(song, **ffmpeg_options, executable="C:\\Users\\jonas\\Documents\\ffmpeg-2022-06-16-git-5242ede48d-full_build\\ffmpeg-2022-06-16-git-5242ede48d-full_build\\bin\\ffmpeg.exe")

            voice_clients[msg.guild.id].play(player)


        if msg.content.startswith(f"{prefix}pause"):
            try:
                voice_clients[msg.guild.id].pause()
            except Exception as err:
                print(err)

        if msg.content.startswith(f"{prefix}resume"):
            try:
                voice_clients[msg.guild.id].resume()
            except Exception as err:
                print(err)

        if msg.content.startswith(f"{prefix}stop"):
            try:
                voice_clients[msg.guild.id].stop()
                await voice_clients[msg.guild.id].disconnect()
            except Exception as err:
                print(err)


client.run(token)
