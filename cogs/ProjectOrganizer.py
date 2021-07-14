import discord
from discord.ext import commands

class Organizer(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def CreateGame(self, ctx, name):
        guild = ctx.guild
        user = ctx.message.author

        role = await guild.create_role(name=f"{name} developer")
        await user.add_roles(role)

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            guild.me: discord.PermissionOverwrite(read_messages=True),
        }
        category = await guild.create_category(name, overwrites=overwrites)
        await category.set_permissions(role, send_messages=True, read_messages=True)

        await guild.create_text_channel("важное-❗", overwrites=None, category=category, reason=None)
        await guild.create_text_channel("основной-🛠", overwrites=None, category=category, reason=None)
        await guild.create_text_channel("беклог-📋", overwrites=None, category=category, reason=None)



        await ctx.send(f"Всё готово! Приятной разработки {name} 👍🏻")

def setup(client):
    client.add_cog(Organizer(client))