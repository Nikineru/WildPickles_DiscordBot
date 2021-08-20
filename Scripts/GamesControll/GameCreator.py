import discord
from Game import Game


class GameCreator:
    def __init__(self, guild, game_name):
        self.Guild = guild
        self.GameName = Game.GetValidName(game_name)
        self.GameRoleName = Game.GetRoleName(game_name)
    
    async def Create(self):
        game_role = await self.Guild.create_role(name=self.GameRoleName)

        overwrites = {
            self.Guild.default_role: discord.PermissionOverwrite(read_messages=False),
            self.Guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True),
        }

        game_category = await self.Guild.create_category(self.GameName, overwrites=overwrites)
        await game_category.set_permissions(game_role, send_messages=True, read_messages=True)

        new_game = Game(self.GameName, game_category, game_role)

        new_game.AddTextChannels("важное-❗", "переговорная-🛠", "беклог-📋", "изменения-🆕")
        new_game.AddVoiceChannels("собрания-🔉")

        for channel in new_game.Channels:
            await channel.initialize(self.Guild, game_category)
        
        return new_game
