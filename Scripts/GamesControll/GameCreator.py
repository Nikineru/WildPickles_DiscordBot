import discord
from GamesControll.GamesData import GameData
from GamesControll.GamesDataBase import DataWorker


class GameCreator:
    def __init__(self, guild, game_name):
        self.Guild = guild
        self.GameData = GameData(game_name)
        self.DataWorker = DataWorker()
    
    async def Create(self):
        game_role = await self.Guild.create_role(name=self.GameData.RoleName)

        overwrites = {
            self.Guild.default_role: discord.PermissionOverwrite(read_messages=False),
            self.Guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True),
        }

        game_category = await self.Guild.create_category(self.GameData.Name, overwrites=overwrites)
        await game_category.set_permissions(game_role, send_messages=True, read_messages=True)

        for channel in self.GameData.Channels:
            await channel.initialize(self.Guild, game_category)
        
        self.DataWorker.SetInfo(self.GameData.Name, game_role.id, game_category.id)
        return self.GameData