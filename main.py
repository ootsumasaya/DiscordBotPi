import discord
import traceback
from discord.ext import commands
from os import getenv
from replit import db
from server import keep_alive

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='/', intents=intents)

@bot.event
async def on_command_error(ctx, error):
    orig_error = getattr(error, "original", error)
    error_msg = ''.join(traceback.TracebackException.from_exception(orig_error).format())
    await ctx.send(error_msg)

@bot.command()
async def ping(ctx):
    await ctx.send('pong')

@bot.command()
async def add(ctx, arg):
    member = str(ctx.author.name)
    delta_payment = int(arg)
    if member not in db.keys():
        db[member] = delta_payment
    else:
        new_payment = db[member] + delta_payment
        db[member] = new_payment
    msg = '\n'.join("{0}:{1}".format(member,payment) for (member,payment) in db.items())
    await ctx.send(msg)

@bot.command()
async def reset(ctx):
  member = str(ctx.author.name)
  del db[member]
  await ctx.send("deleted " + member)
        
@bot.command()
async def show(ctx):
    msg = '\n'.join("{0}:{1}".format(member,payment) for (member,payment) in db.items())
    await ctx.send(msg)

keep_alive()
token = getenv('DISCORD_BOT_TOKEN')
bot.run(token)

