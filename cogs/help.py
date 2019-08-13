import discord
from discord.ext import commands

class Help(commands.Cog):

    def __init__(self, client):
        self.client = client
        client.remove_command('help')
        
    @commands.command()
    async def help(self, ctx):
        embed = discord.Embed(
            title = 'Bot Info',
            description = 'Created by sydney#9966 in June of 2019 for Mind Café.',
            color = discord.Color.teal()
        )
        embed.set_thumbnail(url = 'https://cdn.discordapp.com/emojis/592855049403891713.png')
        embed.add_field(name = 'Hello!',
        value = 'My name is Bean! I\'m a fluffy corgi who\'s here to help the server with lots of stuffies.\nI\'m currently in alpha development, so please forgive me if I start barking in the wrong direction!', inline = True)

        await ctx.send(embed = embed)

def setup(client):
    client.add_cog(Help(client))
