import discord
from discord.ext import commands

class Echo(commands.Cog):

    def __init__(self, client):
        self.client = client

    #discord.TextChannel c = NONE

    @commands.command()
    async def setEchoChannel(self, ctx, channel):
        if 'mods' in [role.name for role in ctx.message.author.roles] or 'mechanic' in [role.name for role in ctx.message.author.roles]:
            if (not(channel in [TextChannel.name for TextChannel in ctx.guild.text_channels])):
                await ctx.send('I can\'t seem to find that channel.')
            else:
                for chn in ctx.guild.text_channels:
                    if chn.name == channel:
                        channel_id = chn.id
                c = ctx.guild.get_channel(channel_id)
        else:
            await ctx.send('You don\'t have the permissions to do that!')

    @commands.Cog.listener()
    async def on_ready(self):
        if ('echo' in [TextChannel.name for TextChannel in ctx.guild.text_channels]):

            print('Echo is ready.')
        else:
            print('No echo channel found.')

def setup(client):
    client.add_cog(Echo(client))
