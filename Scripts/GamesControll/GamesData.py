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

class GameData:
    def __init__(self, name, role_id=0, category_id=0):
        self.Name = self.GetValidName(name)
        self.RoleName = self.GetRoleName()
        self.RoleID = role_id
        self.CategoryID = category_id

        self.Channels = list()
        #self.AddTextChannels("важное-❗", "переговорная-🛠", "беклог-📋", "изменения-🆕")
        self.AddVoiceChannels("собрания-🔉")

    def AddTextChannels(self, *channels_names:str):
        for name in channels_names:
            self.Channels.append(Channel(name, 0))

    def AddVoiceChannels(self, *channels_names:str):
        for name in channels_names:
            self.Channels.append(Channel(name, 1))

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
        return f"{self.Name} developer"