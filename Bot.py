"""
    Discord Robot Earthquake Detection Robot
    開機、核心功能程式 Main Function
"""
"""

    Author  : zong zong
    Connect : zongozngchu0408@gmail.com
    School  : 臺北市立中正高級中學
    GitHub  : https://github.com/zongzong0408/Discord-Robot-Earthquake-Detection-Robot

    Last edited : 2022/10/15/06:00PM

    Bot invite link : https://discord.com/api/oauth2/authorize?client_id=1012673195041636372&permissions=124992&scope=bot

"""
TOKEN = "YOUR DISCORD BOT TOKEN"

import discord as dc
from discord.ext import commands
import os  

intents = dc.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix ="./", intents = intents)

@bot.event
async def on_ready():
    print("robot : < Discord Bot \"fat cat\" is Starting now >\nrunning process : 60 %")
    print(f"robot : running on [ Name : {bot.user.name}, ID : {bot.user.id} ]\nrunning process : 90 %\nrunning process : 100 %")
    print("robot : < open full successfully >")

@bot.event
async def on_connect():
    print("robot : < Discord Bot \"fat cat\" is Online now >\nrunning process : 30 %")

@bot.event
async def on_disconnect():
    print("robot : < Discord Bot \"fat cat\" is Offline now >\nrunning process : 0 %")

@bot.event
async def on_error(ctx, error):
    print("robot : Error ! < Event program has a trouble... >")
    await ctx.send(f"```fix\n{error}\n```")
    print(f"robot : Error ! {error}\n")

@bot.event
async def on_command_error(ctx, error):
    print("robot : Error ! < Command program has a trouble... >")

    if isinstance(error, commands.errors.CommandNotFound):
        await ctx.send(f"```fix\n{error}\n```")
        print(f"robot : Error ! {error}\n")
    
    elif isinstance(error, commands.errors.MissingRequiredArgument):
        await ctx.send(f"```fix\n{error}\n```")
        print(f"robot : Error ! {error}\n")
    
    elif isinstance(error, commands.errors.CommandError):
        await ctx.send(f"```fix\n{error}\n```")
        print(f"robot : Error ! {error}\n")

for FileName in os.listdir('./Commands'):
    if FileName.endswith('.py'):
        bot.load_extension(f'Commands.{FileName[ : -3]}')

@bot.command(aliases = ["l"])
async def load(ctx, extension):
    """
        Load .py file.
    """
    bot.load_extension(f'Commands.{extension}')
    embed = dc.Embed(
        description = "Has been loaded successfully.",
        color = 0x7E3D76
    )
    await ctx.send(embed = embed)

@bot.command(aliases = ["r"])
async def reload(ctx, extension):
    """
        Reload .py file.
    """
    bot.reload_extension(f'Commands.{extension}')
    embed = dc.Embed(
        description = "Has been reloaded successfully.",
        color = 0x7E3D76
    )
    await ctx.send(embed = embed)

@bot.command(aliases = ["u"])
async def unload(ctx, extension):
    """
        Unload .py file.
    """
    bot.unload_extension(f'Commands.{extension}')
    embed = dc.Embed(
        description = "Has been unloaded successfully.",
        color = 0x7E3D76
    )
    await ctx.send(embed = embed)

if  __name__ == "__main__":
    bot.run(TOKEN)