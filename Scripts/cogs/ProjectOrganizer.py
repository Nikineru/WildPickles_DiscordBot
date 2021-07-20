import re
import discord
from discord import utils
from discord.ext import commands


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


class GameRemover:
    def __init__(self, guild, name, role_name):
        self.Guild = guild
        self.RoleName = role_name
        self.Name = name     

    async def Remove(self):
        try:
            game_category = utils.get(self.Guild.categories, name=self.Name)

            for channel in game_category.channels:
                await channel.delete()

            await game_category.delete()
            
            game_role = utils.get(self.Guild.roles, name=self.RoleName)
            await game_role.delete()
            
            return True

        except Exception as exeption:
            print(str(exeption))
            return False


class GameCreator():
    def __init__(self, guild,  name:str, role_name:str):
        self.Guild = guild
        self.Name = name
        self.Channels = list()
        self.AcessRole = None
        self.AcessRoleName = role_name

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

            category = await self.Guild.create_category(self.Name, overwrites=overwrites)
            await category.set_permissions(self.AcessRole, send_messages=True, read_messages=True)

            for channel in self.Channels:
                await channel.initialize(self.Guild, category)

            return True

        except Exception as exeption:
            print(str(exeption))
            return False


class Organizer(commands.Cog):
    def __init__(self, client):
        self.client = client

    def GetValidName(self, text):
        words = text.split()

        for i in range(len(words)):
            word = re.sub(r"\W", "", words[i])
            word = word.replace("_", "")
            words[i] = word

        result = " ".join(words)

        if len(result) < 1:
            result = "default name"

        return result.title()

    def GetRoleName(self, text):
        return f"{self.GetValidName(text)} developer"

    @commands.command()
    async def CreateGame(self, ctx, *name):
        guild = ctx.guild
        user = ctx.message.author
        name = self.GetValidName(" ".join(name))
        role_name = self.GetRoleName(name)
        
        if utils.get(guild.categories, name=name):
            await ctx.send(f"Игра {name} уже разрабатывается 😢")
            return

        if len(guild.categories) > 15:
            await ctx.send("Это похоже на спам 😡")
            return

        creator = GameCreator(guild, name, role_name)

        creator.AddVoiceChannels("переговорная-💼")
        creator.AddTextChannels("важное-❗", "основной-🛠", "беклог-📋")

        CreateStatus = await creator.Create()

        if(CreateStatus):
            await user.add_roles(creator.AcessRole)
            await ctx.send(f"Всё готово! Приятной разработки {creator.Name} 👍🏻")
        else:
            await ctx.send(f"Что-то пошло не так во время создания игры {creator.Name} 😢")

    @commands.command()
    async def RemoveGame(self, ctx, *name):
        guild = ctx.guild
        name = self.GetValidName(" ".join(name))
        remover = GameRemover(guild, name, self.GetRoleName(name))

        RemoveStatus = await remover.Remove()

        if(RemoveStatus):
            await ctx.send(f"Всё готово! Игра {remover.Name} удалена 👍🏻")
        else:
            await ctx.send(f"Что-то пошло не так во время удаления игры {remover.Name} 😢")

def setup(client):
    client.add_cog(Organizer(client))