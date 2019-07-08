import discord
from discord.ext import commands

class Triggers(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message):
        return

def setup(client):
    client.add_cog(Triggers(client))
