from GameCreator import GameCreator
from discord import utils
from discord.ext import commands


class Organizer(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def CreateGame(self, ctx, *name):
        guild = ctx.guild
        user = ctx.message.author
        creator = GameCreator(guild, " ".join(name))

        await creator.Create()
    #@commands.command()
    #async def RemoveGame(self, ctx, *name):
    #    guild = ctx.guild
    #    remover = GameRemover(guild, " ".join(name))

    #    RemoveStatus = await remover.Remove()

    #    if(RemoveStatus):
    #        await ctx.send(f"Всё готово! Игра {remover.GameName} удалена 👍🏻")
    #    else:
    #        await ctx.send(f"Что-то пошло не так во время удаления игры {remover.GameName} 😢")

def setup(client):
    client.add_cog(Organizer(client))