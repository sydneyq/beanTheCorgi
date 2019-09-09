import discord
from discord.ext import commands
from database import Database
from .meta import Meta
import json
import os
import asyncio
import secret
import random
from numpy.random import choice

class Battle(commands.Cog):

    def __init__(self, client, database, meta):
        self.client = client
        self.dbConnection = database
        self.meta = meta

    @commands.command(aliases=['challenge'])
    async def battle(self, ctx, channel: discord.TextChannel = None):
        return
        message = ctx.message
        if not self.meta.isAdmin(message.author):
            return

        if channel is None:
            channel = ctx.channel

        await ctx.message.delete()

        embed = discord.Embed(
            title = 'Game On: Avatar!',
            description = 'Bean is the Avatar and needs teachers from each element!',
            color = discord.Color.teal()
        )

        choices = ['Water', 'Air', 'Fire', 'Earth']
        result = random.choice(choices)
        pic = ''

        if result == 'Water':
            pic = 'http://dpegb9ebondhq.cloudfront.net/product_photos/15204550/water-01_large.jpg'
        elif result == 'Air':
            pic = 'https://d3u67r7pp2lrq5.cloudfront.net/product_photos/15204511/air-01_original.jpg'
        elif result == 'Fire':
            pic = 'https://dzasv7x7a867v.cloudfront.net/product_photos/15204544/Fire-01_original.jpg'
        elif result == 'Earth':
            pic = 'http://d3u67r7pp2lrq5.cloudfront.net/product_photos/15204526/earth-01_400w.jpg'

        embed.add_field(name='Affinity: ' + result, value='Get someone from your Squad with the correct Affinity to post the 💥 emoji before the other Squad to gain a point!')
        embed.set_thumbnail(url = pic)
        await channel.send(embed = embed)

        def check(m):
            return m.content.lower() == '💥' and m.channel == channel

        cont = True

        while (cont):
            msg = await self.client.wait_for('message', check=check)

            user = self.meta.getProfile(msg.author)

            if user['squad'] == '':
                embed = discord.Embed(
                    title = 'Sorry, you\'re not in a Squad yet! Join one by using `+squad tea/coffee`.',
                    color = discord.Color.teal()
                )
                await channel.send(embed = embed)
                cont = True
                continue
            elif user['affinity'] is None or user['affinity'] == '':
                embed = discord.Embed(
                    title = 'Sorry, you haven\'t set an affinity yet! You can do that by using `+affinity fire/water/air/earth`.',
                    color = discord.Color.teal()
                )
                await channel.send(embed = embed)
                cont = True
                continue
            elif user['affinity'] != result:
                embed = discord.Embed(
                    title = 'You don\'t have the required affinity! You\'re looking for someone who\'s `' + result + '`.',
                    color = discord.Color.teal()
                )
                await channel.send(embed = embed)
                cont = True
                continue
            elif user['affinity'] == result:
                cont = False

                squad = user['squad']
                if squad == 'Tea':
                    self.tea_score += 1
                else:
                    self.coffee_score += 1

                embed2 = discord.Embed(
                    title = msg.author.name + ' just earned `1` point for ' + squad + '!',
                    description = '**Tea Squad:** `' + str(self.tea_score) + '`\n**Coffee Squad:** `' + str(self.coffee_score) + '`',
                    color = discord.Color.teal()
                )

                if self.tea_score > self.coffee_score:
                    embed2.set_thumbnail(url = 'https://cdn.discordapp.com/attachments/591611902459641856/613918428293627914/teamteaBean.png')
                elif self.coffee_score > self.tea_score:
                    embed2.set_thumbnail(url = 'https://cdn.discordapp.com/attachments/591611902459641856/613918442034298890/teamcoffeeBean.png')


                await channel.send(embed = embed2)

                return

def setup(client):
    database_connection = Database()
    meta_class = Meta(database_connection)
    client.add_cog(Battle(client, database_connection, meta_class))
