import discord
from discord.utils import get
from GamesControll.GamesData import GameData
from GamesControll.GamesDataBase import DataWorker


class GameRemover:
    def __init__(self, guild, game_name):
        self.Guild = guild
        self.GameData = GameData(game_name)
        self.DataWorker = DataWorker()
    
    async def Remove(self):
        game_data = self.DataWorker.GetInfo(self.GameData.Name)

        category = get(self.Guild.categories, id=game_data.CategoryID)

        for channel in category.channels:
            await channel.delete()

        await category.delete()
        await get(self.Guild.roles, id=game_data.RoleID).delete()
        self.DataWorker.DeleteInfo(self.GameData.Name)