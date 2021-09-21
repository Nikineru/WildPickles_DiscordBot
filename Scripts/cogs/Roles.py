import discord
from discord.ext import commands

class Organizer(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        if(before.roles != after.roles):
            pass

def setup(client):
    client.add_cog(Organizer(client))