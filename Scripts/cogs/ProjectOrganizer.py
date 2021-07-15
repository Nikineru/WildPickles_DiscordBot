import discord
from discord.ext import commands


class Channel:
    def __init__(self, name, type:int, access_role=None): # type (0 - текстовый, 1 - голосовой)
        self.Name = name
        self.Type = type
        self.AccessRole = access_role
            
    async def initialize(self, guild, category):
        if(self.Type == 0):
            await guild.create_text_channel(self.Name, category=category)
        else:
            await guild.create_voice_channel(self.Name, category=category)


class Game:
    def __init__(self):
        self.Name = "default name"
        self.AccessRole=None
        self.Channels = list()

    def SetName(self, name:str):
        self.Name = name

    def AddTextChannels(self, *channels_names:str):
        for name in channels_names:
            self.Channels.append(Channel(name, 0))

    def AddVoiceChannels(self, *channels_names:str):
        for name in channels_names:
            self.Channels.append(Channel(name, 1))

    def GetRoleName(self):
        return f"{self.Name} developer"

    async def GetSameGames(self, guild):
        categories = guild.categories

        for category in categories:
            if category.name == self.Name:
                return False
        
        return True

    async def RemoveGame(self, guild):
        categories = guild.categories

        for category in categories:
            if category.name == self.Name:
                for channel in category.channels:
                    channel.delete()

            category.delete()

        self.AccessRole.delete()


    async def Initialize(self, guild):
        try:
            self.AccessRole = await guild.create_role(name=self.GetRoleName())

            overwrites = {
                guild.default_role: discord.PermissionOverwrite(read_messages=False),
                guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True),
            }

            category = await guild.create_category(self.Name, overwrites=overwrites)
            await category.set_permissions(self.AccessRole, send_messages=True, read_messages=True)

            for channel in self.Channels:
                await channel.initialize(guild, category)

            return True

        except Exception as exeption:
            print(str(exeption))
            return False


class Organizer(commands.Cog):
    def __init__(self, client):
        self.client = client

        self.GamePrefab = Game()
        self.GamePrefab.AddTextChannels("важное-❗", "основной-🛠", "беклог-📋")
        self.GamePrefab.AddVoiceChannels("переговорная-💼")

    @commands.command()
    async def CreateGame(self, ctx, name):
        guild = ctx.guild
        user = ctx.message.author

        self.GamePrefab.SetName(name)

        if(await self.GamePrefab.IsOriginal(guild) is False):
            await ctx.send(f"К сожалению игра {name} уже разрабатывается")
            return

        InitializeStatus = await self.GamePrefab.Initialize(guild)

        if(InitializeStatus is True):
            await user.add_roles(self.GamePrefab.AccessRole)
            await ctx.send(f"Всё готово! Приятной разработки {self.GamePrefab.Name} 👍🏻")
        else:
            await ctx.send("Что-то пошло не по планам 😢")

    @commands.command()
    async def DeleteGame(self, ctx, name):#TODO
        guild = ctx.guild
        self.GamePrefab.SetName(name)
        await self.GamePrefab.RemoveGame(guild)

def setup(client):
    client.add_cog(Organizer(client))