import re

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

class Game:
    def __init__(self, name, category, role):
        self.Name = name,
        self.RoleID = role
        self.Channels = list(),
        self.CategoryID = category,

    def AddTextChannels(self, *channels_names:str):
        for name in channels_names:
            self.Channels.append(Channel(name, 0))

    def AddVoiceChannels(self, *channels_names:str):
        for name in channels_names:
            self.Channels.append(Channel(name, 1))

    @staticmethod
    def GetValidName(text):
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

    @staticmethod
    def GetRoleName(name):
        return f"{name} developer"