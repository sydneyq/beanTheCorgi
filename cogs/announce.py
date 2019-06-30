import discord
from discord.ext import commands

class Announce(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def verify(self, ctx):
        if 'mechanic' in [role.name for role in ctx.message.author.roles]:
            embed = discord.Embed(
                color = discord.Color.teal(),
                title = '**Welcome to Mind Café!**',
                description = 'Be sure to read `#commandments` for our server rules.'
            )

            embed.set_footer(text = 'Thanks for joining our family!')
            embed.set_thumbnail(url = 'https://cdn.discordapp.com/emojis/593214693573787654.png')

            embed.add_field(name = '**You are currently unverified.**',
            value = 'Please take a second to verify yourself by saying: `?verify`\n\nAsk a Mod if you need assistance!')

            await ctx.send(embed = embed)
        else:
            embed = discord.Embed(
                title = 'Sorry, you don\'t have permission to do that!',
                color = discord.Color.teal()
            )
            await ctx.send(embed = embed)

def setup(client):
    client.add_cog(Announce(client))
