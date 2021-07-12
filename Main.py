import discord
from discord.ext import commands
from Token import TOKEN

client = commands.Bot(command_prefix = '!')

@client.event
async def on_message(message):
    if message.author.bot:
        return

    await client.process_commands(message)

@client.command()
async def Greet(ctx):
    await ctx.send(ctx.message.author.name)

client.run(TOKEN)