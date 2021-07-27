import discord


class Organizer(commands.Cog):
    def __init__(self, client):
        self.client = client


def setup(client):
    client.add_cog(Organizer(client))