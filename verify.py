import discord
import ctypes
from discord.ext import commands
from discord.utils import get        
from discord.ext.commands import bot
import requests
import asyncio
intents = discord.Intents(messages=True, guilds=True, members=True)
intents.dm_messages=True
intents.members = True
intents.guild_messages=True

client = commands.Bot(command_prefix = ".", intents=intents)
client.remove_command('help')
async def status_task():
    while(True):
        await client.change_presence(status=discord.Status.dnd, activity=discord.Game("use .verify"))
        await asyncio.sleep(10)
        await client.change_presence(status=discord.Status.dnd, activity=discord.Game("sellix.io/ETSB"))
        await asyncio.sleep(10)
        await client.change_presence(status=discord.Status.dnd, activity=discord.Game("eintim.ga/dashboard"))
        await asyncio.sleep(10)
        await client.change_presence(status=discord.Status.dnd, activity=discord.Game("for help visit: docs.eintim.ga"))
        await asyncio.sleep(10)
@client.event
async def on_ready():
    print("bot ready")
    client.loop.create_task(status_task())
@client.event
async def on_message(ctx):
    msg = ctx.content
    if ctx.content == ".verify":
        if isinstance(ctx.channel, discord.channel.DMChannel):
            embed = discord.Embed(title="Verification started!", description="Now send your username in the chat.", color=0x800000)
            embed.set_footer(text="EinTim verify bot" )
            await ctx.channel.send(embed=embed)
            await asyncio.sleep(0.3)
            resuser = await client.wait_for("message", check=lambda message: message.author == ctx.author)
            embed = discord.Embed(title="Password check", description="Now send your password in the chat.", color=0x800000)
            embed.set_footer(text="EinTim verify bot" )
            await ctx.channel.send(embed=embed)
            await asyncio.sleep(0.3)
            respass = await client.wait_for("message", check=lambda message: message.author == ctx.author)
            r = requests.get(f"https://eintim.ga/dashboard/api/verify.php?user={resuser.content}&pass={respass.content}")
            if r.content == b'uhjfefdyaiu':
                guild = client.get_guild(774334632274952192)
                user = guild.get_member(ctx.author.id)
                role = get(client.get_guild(774334632274952192).roles, id=817370368586022942)
                await user.add_roles(role)
                embed = discord.Embed(title="Verification completed!", description="You now have the customer role on the discord", color=0x800000)
                embed.set_thumbnail(url="https://media.discordapp.net/attachments/757680548213686272/759077346346139698/check.gif")
                embed.set_footer(text="EinTim verify bot" )
                await ctx.channel.send(embed=embed)
            else:
                embed = discord.Embed(title="Verification aborted!", description="Wrong username or password", color=0x800000)
                embed.set_footer(text="EinTim verify bot" )
                await ctx.channel.send(embed=embed)
        else:
            await ctx.delete()
            embed = discord.Embed(title="Please pm me", description="Dont use the public chat to verify!", color=0x800000)
            embed.set_footer(text="EinTim verify bot")
            await ctx.channel.send(embed=embed)

client.run("token")