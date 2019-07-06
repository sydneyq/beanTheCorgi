import discord
from discord.ext import commands
#channelID = 593153723610693632

class Echo(commands.Cog):
    channelID = 593153723610693632

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def echo(self, ctx, channel: discord.TextChannel, *, message):
        if 'Halo' in [role.name for role in ctx.message.author.roles] or 'mechanic' in [role.name for role in ctx.message.author.roles]:

            embed = discord.Embed(
                title = 'A Mind Café Staff Member Says:',
                description = message,
                color = discord.Color.teal()
            )

            #await channel.send("**Staff Member:** " + message)
            #self.client.send_message(channel, embed=embed)
            await channel.send(embed = embed)
        else:
            embed = discord.Embed(
                title = 'Sorry, you don\'t have permission to do that!',
                color = discord.Color.teal()
            )
            await ctx.send(embed = embed)

    @commands.command()
    async def bean(self, ctx, channel: discord.TextChannel, *, message):
        if 'mechanic' in [role.name for role in ctx.message.author.roles]:

            embed = discord.Embed(
                description = message,
                color = discord.Color.teal()
            )

            await channel.send(embed = embed)
        else:
            embed = discord.Embed(
                title = 'Sorry, you don\'t have permission to do that!',
                color = discord.Color.teal()
            )
            await ctx.send(embed = embed)

def setup(client):
    client.add_cog(Echo(client))
