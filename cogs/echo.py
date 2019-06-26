import discord
from discord.ext import commands
#channelID = 593153723610693632

class Echo(commands.Cog):
    channelID = 593153723610693632

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def echo(self, ctx, channel: discord.TextChannel, *, message):
        if '*' in [role.name for role in ctx.message.author.roles] or 'mechanic' in [role.name for role in ctx.message.author.roles]:
            embed = discord.Embed(
                title = 'A Mind Café Staff Member Says:',
                description = message,
                color = discord.Color.teal()
            )

            await channel.send("**A Mind Café Staff Member Says:**\n" + message)#[1:])
            #self.client.send_message(channel, embed=embed)
            #await ctx.send(embed = embed)
        else:
            embed = discord.Embed(
                title = 'Sorry, you don\'t have permission to do that!',
                color = discord.Color.teal()
            )
            await ctx.send(embed = embed)

def setup(client):
    client.add_cog(Echo(client))
