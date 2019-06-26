import discord
from discord.ext import commands

class AnnounceVerify(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def announceverify(self, ctx):
        if 'mechanic' in [role.name for role in ctx.message.author.roles]:
            embed = discord.Embed(
                color = discord.Color.teal(),
                title = '**Welcome to Mind Café!**',
                description = 'Be sure to read #commandments for our server rules.'
            )

            embed.set_footer(text = 'Thanks for joining our family!')
            embed.set_thumbnail(url = 'https://cdn.discordapp.com/emojis/593214693573787654.png')

            embed.add_field(name = '**You are currently unverified.**',
            value = 'Please take a second to verify yourself by __reacting to this message with the :beanVV: emoji.__\n\nIt should already be down for you below, but if you can\'t see it or add it, message an Angel or Guardian and they can verify you manually.')

            await ctx.send(embed = embed)
        else:
            await ctx.send('You don\'t have the permissions to do that!')

def setup(client):
    client.add_cog(AnnounceVerify(client))
