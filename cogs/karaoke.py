import discord
from discord.ext import commands

class MsgPersist(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.queue = list()

    @commands.Cog.listener()
    async def on_message(self, message):
        if ('karaoke' in message.channel.name):
            id = message.author.id
            if ('add me' in message.content.lower()):
                if id not in self.queue:
                    self.queue.append(id)
                    embed = discord.Embed(
                        title = 'Added you to the queue!',
                        color = discord.Color.teal()
                    )
                    await message.channel.send(embed = embed)
                else:
                    embed = discord.Embed(
                        title = 'You\'re already in the queue!',
                        color = discord.Color.teal()
                    )
                    await message.channel.send(embed = embed)
            elif ('remove me' in message.content.lower()):
                if id in self.queue:
                    embed = discord.Embed(
                        title = 'I\'ve removed you from the queue.',
                        color = discord.Color.teal()
                    )
                    await message.channel.send(embed = embed)

                    '''
                    if (len(self.queue) > 1 and self.queue.index(id) == 0):
                        embed2 = discord.Embed(
                            title = 'Next person: ' + self.queue[1],
                            color = discord.Color.teal()
                        )
                        await message.channel.send(embed = embed2)
                    '''

                    self.queue.remove(id)
                else:
                    embed = discord.Embed(
                        title = 'You\'re not in the queue!',
                        color = discord.Color.teal()
                    )
                    await message.channel.send(embed = embed)
            elif ('queue' in message.content.lower()):
                say = ''

                for id in self.queue:
                    say += self.client.get_user(id).name + '\n'
                embed = discord.Embed(
                    title = 'Current Queue',
                    color = discord.Color.teal(),
                    description = say
                )
                await message.channel.send(embed = embed)
            elif 'skip' == message.content.lower() and ('angels' in [role.name for role in message.author.roles] or 'mechanic' in [role.name for role in message.author.roles]):
                self.queue.pop()
                embed = discord.Embed(
                    title = 'I\'ve skipped to the next person.',
                    color = discord.Color.teal()
                )
                await message.channel.send(embed = embed)
                self.queue.remove(id)

def setup(client):
    client.add_cog(MsgPersist(client))
