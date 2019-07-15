import discord
from discord.ext import commands
import asyncio
from itertools import cycle

import requests
import random
from random import randint

class Timers(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.client.loop.create_task(self.dailyHello())

    @commands.Cog.listener()
    async def dailyHello(self):
        await self.client.wait_until_ready()

        guild = self.client.get_guild(257751892241809408)
        channel = guild.get_channel(298245133038649345)
        members = guild.members

        #await channel.send('Ready!')

        msgs = ['We hope you\'re having a great day, and remember that we\'re always here for you when you\'re struggling.']
        imgs = ['https://media0.giphy.com/media/DcKEISp6FJSqQ/giphy.gif',
        'https://i.imgur.com/KzPnrV0.gif',
        'https://media2.giphy.com/media/xT9DPsQBUcmdKjuzE4/source.gif',
        'https://33.media.tumblr.com/a8c6c5ba1dacbf28c75c0e8662003c48/tumblr_o0d18kutFc1qc4uvwo1_r1_500.gif',
        'https://media1.tenor.com/images/950a1416557b942ba1d81e427a621319/tenor.gif?itemid=12275825',
        'https://i.gifer.com/DW0A.gif',
        'https://media0.giphy.com/media/xUPGcICvRWCEltacNi/source.gif',
        'https://media.giphy.com/media/26xBSxisb1xYv1dja/giphy.gif',
        'https://i.pinimg.com/originals/60/08/20/600820c302000e35b171af5f99a7a71d.gif',
        'https://66.media.tumblr.com/a1525366551f825189cc452999f5ecb8/tumblr_nz4n2v3cBe1sffmwho1_500.gif']

        #member = cycle(members)
        #member = random.choice(members)

        while True:
            member = random.choice(members)

            while (member.bot):
                member = random.choice(members)

            await channel.send('__**Hello, <@' + str(member.id) + '>!**__\nYou\'re today\'s chosen one! Just a little reminder that you\'re amazing.')

            embed = discord.Embed(
                title = random.choice(msgs),
                color = discord.Color.magenta()
            )
            embed.set_image(url = random.choice(imgs))
            await channel.send(embed = embed)

            members = guild.members
            await asyncio.sleep(86400)


def setup(client):
    #client.loop.create_task(dailyHello())
    client.add_cog(Timers(client))
