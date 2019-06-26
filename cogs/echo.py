import discord
from discord.ext import commands
#channelID = 593153723610693632

class Echo(commands.Cog):
    channelID = 593153723610693632

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def getEchoChannel(self, ctx):
        if 'mods' in [role.name for role in ctx.message.author.roles] or 'mechanic' in [role.name for role in ctx.message.author.roles]:
            global channelID
            await ctx.send('Current echo channel: <#' + str(channelID) + '>')
        else:
            await ctx.send('You don\'t have the permissions to do that!')

    @commands.command()
    async def setEchoChannel(self, ctx, channel: discord.TextChannel):
        if 'mods' in [role.name for role in ctx.message.author.roles] or 'mechanic' in [role.name for role in ctx.message.author.roles]:
            '''
            if (self.client.get_channel(channel) == None and not(channel in ctx.guild.text_channels)):
                await ctx.send('I can\'t seem to find that channel.')
            else:
                for chn in ctx.guild.text_channels:
                    if chn == channel:
                        channel_id = chn.id
                c = ctx.guild.get_channel(channel_id)
                await ctx.send('Channel set to' + c)
            '''

            global channelID
            channelID = channel.id
            await ctx.send('Channel set to <#' + str(channelID) + '>!')
        else:
            await ctx.send('You don\'t have the permissions to do that!')

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        #yield from self.client.process_commands(message)
        global channelID

        if message.channel.name == 'echo' and ('angels' in [role.name for role in message.author.roles] or 'mechanic' in [role.name for role in message.author.roles]):
            if not(message.content.startswith('+')): #and message.content.startswith('.'):

                channelRef = self.client.get_channel(257751892241809408)
                '''
                embed = discord.Embed(
                    title = 'A Mind Café Staff Member Says:',
                    description = message.content,
                    color = discord.Color.teal()
                )
                '''
                #await discord.Client().send_message(channelRef, embed=embed)
                await channelRef.send("**A Mind Café Staff Member Says:**\n" + message.content)#[1:])
                #await ctx.send(embed = embed)

        #if ('echo' in [TextChannel.name for TextChannel in ctx.guild.text_channels]):
        '''
            print('Echo is ready.')
        else:
            print('No echo channel found.')
        '''

def setup(client):
    client.add_cog(Echo(client))
