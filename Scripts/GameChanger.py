import re
import discord


class Channel:
    def __init__(self, name, type:int, access_role=None): # type (0 - текстовый, 1 - голосовой)
        self.Name = name
        self.Type = type
        self.AcessRole = access_role
            
    async def initialize(self, guild, category):
        if(self.Type == 0):
            await guild.create_text_channel(self.Name, category=category)
        else:
            await guild.create_voice_channel(self.Name, category=category)


class GameChanger:
    def __init__(self, guild, game_name):
        self.Guild = guild
        self.GameName = self.GetValidName(game_name)
        self.AcessRoleName = self.GetRoleName()

    def GetValidName(self, text):
        words = text.split()

        for i in range(len(words)):
            word = re.sub(r"\W", "", words[i])
            word = word.replace("_", "")

            if len(word) < 1:
                words.pop(i)
            else:
                words[i] = word

        result = " ".join(words)

        if len(result) < 1:
            result = "default name"

        return result.title()

    def GetRoleName(self):
        return f"{self.GameName} developer"

    async def GetCategory(self):
        for category in self.Guild.categories:
            if self.GetValidName(category.name) == self.GameName:
                return category
    
    async def GetRole(self):
        for role in self.Guild.roles:
            if role.name == self.AcessRoleName:
                return role


class GameRemover(GameChanger):
    async def Remove(self):
        try:
            game_category = await self.GetCategory()

            for channel in game_category.channels:
                await channel.delete()

            await game_category.delete()
            
            game_role = await self.GetRole()
            await game_role.delete()
            
            return True

        except Exception as exeption:
            print(str(exeption))
            return False


class GameCreator(GameChanger):
    def __init__(self, guild,  name:str):
        super().__init__(guild, name)
        self.Channels = list()
        self.AcessRole = None

    def AddTextChannels(self, *channels_names:str):
        for name in channels_names:
            self.Channels.append(Channel(name, 0))

    def AddVoiceChannels(self, *channels_names:str):
        for name in channels_names:
            self.Channels.append(Channel(name, 1))

    async def Create(self):
        try:
            self.AcessRole = await self.Guild.create_role(name=self.AcessRoleName)

            overwrites = {
                self.Guild.default_role: discord.PermissionOverwrite(read_messages=False),
                self.Guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True),
            }

            category = await self.Guild.create_category(self.GameName, overwrites=overwrites)
            await category.set_permissions(self.AcessRole, send_messages=True, read_messages=True)

            for channel in self.Channels:
                await channel.initialize(self.Guild, category)

            return True

        except Exception as exeption:
            print(str(exeption))
            return False