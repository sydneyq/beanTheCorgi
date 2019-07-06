import discord
from discord.ext import commands

class Triggers(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message):
        if ('i am satisfied with my care' in message.content.lower() or 'i\'m satisfied with my care' in message.content.lower()):
            guild = self.client.get_guild(257751892241809408)
            channel = message.channel

            if channel.name.startswith('s-'):
                userID = int(channel.name[channel.name.rfind('-')+1:])
                if (userID == message.author.id):
                    for ch in guild.text_channels:
                        if ch.name.lower() == 'log':
                            log = guild.get_channel(ch.id)
                            await log.send('Support Ticket [**' + channel.name + '**] has been archived.')
                            break

                    guild = self.client.get_guild(257751892241809408) #Mind Café
                    category = 0

                    for c in guild.categories:
                        if c.name.lower() == 'archive':
                            category = c #Archive

                    #ctx.message.channel.category = 596988830435770368
                    await message.channel.edit(category = category, sync_permissions = True)
                else:
                    embed = discord.Embed(
                        title = 'Sorry, you don\'t have permission to do that!',
                        color = discord.Color.teal()
                    )
                    await ctx.send(embed = embed)
            else:
                embed = discord.Embed(
                    title = 'This doesn\'t seem to be a Support Ticket channel...',
                    color = discord.Color.teal()
                )
                await ctx.send(embed = embed)


def setup(client):
    client.add_cog(Triggers(client))
