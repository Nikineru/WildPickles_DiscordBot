from discord import *

async def SendErrorEmbed(ctx, text='Что-то пошло не так 🤔'):
    embed = Embed(title="Ошибка", description=text, color=Color.red())
    return await ctx.send(embed=embed)

async def SendSuccsesEmbed(ctx, text:str):
    embed = Embed(title="Успешно", description=text, color=Color.green())
    return await ctx.send(embed=embed)