import discord
import Logger
from Token import TOKEN
from discord.ext import commands

client = commands.Bot(command_prefix = '!')

@client.event
async def on_ready():
    print('Connected')
    client.load_extension('cogs.ProjectOrganizer')
    client.load_extension('cogs.Music')

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

@client.command(aliases=['call', 'spam'])
async def Call(ctx, user:discord.User, *text):
    for i in range(5):
        await ctx.send(f"{user.mention} {' '.join(text)}")

@client.command()
async def Ping(ctx):
    await ctx.send("Pong!")

client.run(TOKEN)