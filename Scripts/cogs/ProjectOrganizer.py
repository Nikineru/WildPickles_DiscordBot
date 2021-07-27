from GameChanger import *
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
        

        if await creator.GetCategory() is not None:
            await ctx.send(f"Игра {creator.GameName} уже разрабатывается 😢")
            return

        creator.AddVoiceChannels("переговорная-💼")
        creator.AddTextChannels("важное-❗", "основной-🛠", "беклог-📋")

        CreateStatus = await creator.Create()

        if(CreateStatus):
            await user.add_roles(creator.AcessRole)
            await ctx.send(f"Всё готово! Приятной разработки {creator.GameName} 👍🏻")
        else:
            await ctx.send(f"Что-то пошло не так во время создания игры {creator.GameName} 😢")

    @commands.command()
    async def RemoveGame(self, ctx, *name):
        guild = ctx.guild
        remover = GameRemover(guild, " ".join(name))

        RemoveStatus = await remover.Remove()

        if(RemoveStatus):
            await ctx.send(f"Всё готово! Игра {remover.GameName} удалена 👍🏻")
        else:
            await ctx.send(f"Что-то пошло не так во время удаления игры {remover.GameName} 😢")

def setup(client):
    client.add_cog(Organizer(client))