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

class TempEvent(commands.Cog):

    def __init__(self, client, database, meta):
        self.client = client
        self.dbConnection = database
        self.meta = meta
        self.tea_score = 0
        self.coffee_score = 0

        dirname = os.path.dirname(__file__)
        filename2 = os.path.join(dirname, 'docs/emojis.json')
        filename3 = os.path.join(dirname, 'docs/ids.json')

        with open(filename2) as json_file:
            self.emojis = json.load(json_file)

        with open(filename3) as json_file:
            self.ids = json.load(json_file)

    @commands.command(aliases=['changepts'])
    async def changePoints(self, ctx, squad, pts:int):
        if not self.meta.isBotOwner(ctx.author):
            return
        else:
            if squad == 'Coffee':
                self.coffee_score = pts
            elif squad == 'Tea':
                self.tea_score = pts
            await ctx.send(embed = self.meta.embedDone())

    @commands.command(aliases=['influence', 'justsayit', 'repeatafterme'])
    async def influencer(self, ctx):
        if not self.meta.isAdmin(ctx.author):
            return

        #tea_words = ['leaf', 'teapot']
        #coffee_words = ['latte', 'creamer']

        tea_words = ['stripe', #1
        'calm', #2
        'engine', #3
        'line', #4
        'feather', #5
        'trust', #6
        'smith', #7
        'west', #8
        'ripe', #9
        'frame', #10
        'town', #11
        'prime', #12
        'parachute', #13
        'charge', #14
        'dry']
        coffee_words = ['drop', #1
        'hero', #2
        'invent', #3
        'hint', #4
        'mime', #5
        'film', #6
        'blink', #7
        'phil', #8
        'bury', #9
        'wheat', #10
        'catch', #11
        'against', #12
        'plate', #13
        'slide', #14
        'easter']

        guild = ctx.guild
        tea_index = 0
        coffee_index = 0
        influencer_channel = guild.get_channel(622465906152570880)
        tea_channel = guild.get_channel(self.ids['SQUAD_TEA_CHANNEL'])
        coffee_channel = guild.get_channel(self.ids['SQUAD_COFFEE_CHANNEL'])
        #tea_channel = guild.get_channel(self.ids['WORKSHOP_CHANNEL'])
        #coffee_channel = guild.get_channel(self.ids['WORKSHOP_CHANNEL'])
        tea_icon = 'https://cdn.discordapp.com/attachments/591611902459641856/613918428293627914/teamteaBean.png'
        coffee_icon = 'https://cdn.discordapp.com/attachments/591611902459641856/613918442034298890/teamcoffeeBean.png'

        def embedNext(squad, word):
            nonlocal tea_icon
            nonlocal coffee_icon

            url = tea_icon
            if squad == 'Coffee':
                url = coffee_icon

            embed = discord.Embed(
                title = 'Game On: Influencer!',
                description = 'Get the other team to say your word! Be careful, they\'ll be trying to get one of your members to say theirs!',
                color = discord.Color.teal()
            )
            embed.add_field(name='Your new word is: `' + word + '`', value='If the word is in another word or mixed capitals, it still counts!')
            embed.set_thumbnail(url = url)
            return embed
        '''
        def embedPoint(squad):
            nonlocal tea_icon
            nonlocal coffee_icon

            url = tea_icon
            enemy_squad = 'Coffee'

            if squad == 'Coffee':
                url = coffee_icon
                enemy_squad = 'Tea'

            embed = discord.Embed(
                title = 'Point!',
                description = '+1 point to ' + squad + '!\n' + message.jump_url,
                color = discord.Color.teal()
            )
            embed.add_field(name='Current Points', value='Tea Squad: `' + str(self.tea_score) + '`\nCoffee Squad: `' + str(self.coffee_score) + '`')
            embed.set_thumbnail(url = url)
            return embed
            '''

        def embedGotcha(squad, message, word):
            nonlocal tea_icon
            nonlocal coffee_icon

            url = tea_icon
            enemy_squad = 'Coffee'

            if squad == 'Coffee':
                url = coffee_icon
                enemy_squad = 'Tea'

            embed = discord.Embed(
                title = squad + ' got ' + message.author.name + ' from ' + enemy_squad + ' to say their word, `' + word + '`!',
                description = '+1 point to ' + squad + '!\n' + message.jump_url,
                color = discord.Color.teal()
            )
            embed.add_field(name='Current Points', value='Tea Squad: `' + str(self.tea_score) + '`\nCoffee Squad: `' + str(self.coffee_score) + '`')
            embed.set_thumbnail(url = url)
            return embed

        def embedWon(squad):
            nonlocal tea_icon
            nonlocal coffee_icon

            url = tea_icon
            enemy_squad = 'Coffee'

            if squad == 'Coffee':
                url = coffee_icon
                enemy_squad = 'Tea'

            embed = discord.Embed(
                title = squad + ' got ' + enemy_squad + ' to say all their words!',
                description = 'Congratulations to the ' + squad + ' Squad! ' + self.emojis['Trophy'],
                color = discord.Color.teal()
            )
            embed.set_thumbnail(url = url)
            return embed

        await tea_channel.send(embed = embedNext('Tea', tea_words[tea_index]))
        await coffee_channel.send(embed = embedNext('Coffee', coffee_words[coffee_index]))

        while (tea_index < len(tea_words) and coffee_index < len(coffee_words)):
            tea_trigger = False
            coffee_trigger = False

            def check(m):
                #tea got a coffee to say it?
                nonlocal tea_trigger
                tea_trigger = tea_words[tea_index] in m.content.lower()
                #coffee got a tea to say it?
                nonlocal coffee_trigger
                coffee_trigger = coffee_words[coffee_index] in m.content.lower()
                #check is in public channel
                return (tea_trigger or coffee_trigger) and m.channel.category_id == 363477215377358848

            msg = await self.client.wait_for('message', check=check)

            user = self.meta.getProfile(msg.author)
            squad = user['squad']
            if squad == '':
                continue
            if tea_trigger and squad == 'Coffee':
                self.tea_score += 1
                await msg.channel.send(embed = embedGotcha('Tea', msg, tea_words[tea_index]))
                await influencer_channel.send(embed = embedGotcha('Tea', msg, tea_words[tea_index]))
                tea_index += 1
                if tea_index >= len(tea_words):
                    await influencer_channel.send(embed = embedWon('Tea'))
                await tea_channel.send(embed = embedNext('Tea', tea_words[tea_index]))
                continue
            elif coffee_trigger and squad == 'Tea':
                self.coffee_score += 1
                await msg.channel.send(embed = embedGotcha('Coffee', msg, coffee_words[coffee_index]))
                await influencer_channel.send(embed = embedGotcha('Coffee', msg, coffee_words[coffee_index]))
                coffee_index += 1
                if coffee_index >= len(coffee_words):
                    await influencer_channel.send(embed = embedWon('Coffee'))
                    return
                await coffee_channel.send(embed = embedNext('Coffee', coffee_words[coffee_index]))
                continue
            else:
                continue

    @commands.command(aliases=['pts'])
    async def points(self, ctx):
        embed2 = discord.Embed(
            title = 'Squad Points',
            description = self.emojis['Tea'] + ' **Tea Squad:** `' + str(self.tea_score) + '`\n' + self.emojis['Coffee'] + ' **Coffee Squad:** `' + str(self.coffee_score) + '`',
            color = discord.Color.teal()
        )

        if self.tea_score > self.coffee_score:
            embed2.set_thumbnail(url = 'https://cdn.discordapp.com/attachments/591611902459641856/613918428293627914/teamteaBean.png')
        elif self.coffee_score > self.tea_score:
            embed2.set_thumbnail(url = 'https://cdn.discordapp.com/attachments/591611902459641856/613918442034298890/teamcoffeeBean.png')

        await ctx.send(embed = embed2)

def setup(client):
    database_connection = Database()
    meta_class = Meta(database_connection)
    client.add_cog(TempEvent(client, database_connection, meta_class))
