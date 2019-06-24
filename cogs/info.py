import discord
from discord.ext import commands

class Info(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def info(self, ctx):
        await ctx.send('(Info)')

def setup(client):
    client.add_cog(Info(client))
