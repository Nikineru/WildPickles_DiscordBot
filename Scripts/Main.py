import discord
from discord import channel
from discord.ext import commands
from Token import TOKEN

client = commands.Bot(command_prefix = '!')

@client.event
async def on_ready():
    print('Connected')
    client.load_extension('cogs.ProjectOrganizer')

@client.event
async def on_message(message):
    if message.author.bot:
        return

    await client.process_commands(message)

@client.command()
async def Clear(ctx, number):
    messages = await ctx.channel.history(limit=int(number) + 1).flatten()

    for message in messages:
        await message.delete()

@client.command()
async def Ping(ctx):
    await ctx.send("Pong!")

client.run(TOKEN)