from discord.ext import commands
from GamesControll.GameCreator import GameCreator
from GamesControll.GameRemover import GameRemover

class Organizer(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def CreateGame(self, ctx, *name):
        guild = ctx.guild
        user = ctx.message.author

        creator = GameCreator(guild, " ".join(name))
        game_data = await creator.Create()
        await ctx.send("Игра успешно инициализорована 👍")
    
    @commands.command()
    async def RemoveGame(self, ctx, *name):
        guild = ctx.guild
        user = ctx.message.author

        remover = GameRemover(guild, " ".join(name))
        await remover.Remove()
        await ctx.send("Игра успешно удалена 👍")

def setup(client):
    client.add_cog(Organizer(client))