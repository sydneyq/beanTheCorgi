import discord
from discord.ext import commands
from database import Database
from .meta import Meta
import json
import os
import asyncio
import random
import secret

class Soulmates(commands.Cog):

    def __init__(self, client, database, meta):
        self.client = client
        self.dbConnection = database
        self.meta = meta

        dirname = os.path.dirname(__file__)
        filename = os.path.join(dirname, 'docs/store.json')
        filename2 = os.path.join(dirname, 'docs/emojis.json')
        filename3 = os.path.join(dirname, 'docs/ids.json')

        with open(filename) as json_file:
            self.store = json.load(json_file)

        with open(filename2) as json_file:
            self.emojis = json.load(json_file)

        with open(filename3) as json_file:
            self.ids = json.load(json_file)

    @commands.command(aliases=['spouses', 'spouse', 'soulmate', 'marriages', 'sm'])
    async def soulmates(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author

        user = self.meta.getProfile(member)
        soulmates = user['soulmates']

        num = self.meta.getNumSoulmates(member)
        soulmate_spots = self.meta.getSoulmateSpots(member)
        desc = ''

        for soulmate in soulmates:
            desc += '<@' + str(soulmate) + '>\n'
        if desc == '':
            desc = 'N/A'

        embed = discord.Embed(
            title = member.name + '\'s Soulmates `[' + str(num) + '/' + str(soulmate_spots)  + ']`',
            description = desc,
            color = discord.Color.teal()
        )
        embed.set_footer(text = 'For every 10 Help Points, you gain a soulmate spot!')
        await ctx.send(embed = embed)
        return

    @commands.command(aliases=['propose'])
    async def marry(self, ctx, member: discord.Member = None):
        if member is None:
            embed = discord.Embed(
                description = 'Correct Usage: `+marry @user`.',
                color = discord.Color.teal()
            )
            await ctx.send(embed = embed)
            return

        if ctx.author.bot or member.bot:
            embed = discord.Embed(
                title = 'You can\'t marry a bot!',
                color = discord.Color.teal()
            )
            await ctx.send(embed = embed)
            return
        if member == ctx.author:
            embed = discord.Embed(
                title = 'You can\'t marry yourself!',
                color = discord.Color.teal()
            )
            await ctx.send(embed = embed)
            return

        id = ctx.author.id

        user = self.meta.getProfile(ctx.author)
        memberProfile = self.meta.getProfile(member)

        if not self.meta.canAddSoulmate(ctx.author) or not self.meta.canAddSoulmate(member):
            embed = discord.Embed(
                title = 'One of you doesn\'t have enough soulmate spots!',
                color = discord.Color.teal()
            )
            await ctx.send(embed = embed)
            return

        embed = discord.Embed(
            title = ctx.author.name + ' proposed to ' + member.name + '!',
            description = 'React to this message with a ❤ for yes, 💔 for no.\nYou have 60 seconds to decide!',
            color = discord.Color.teal()
        )
        await ctx.send(embed = embed)

        msg = ctx.channel.last_message
        await msg.add_reaction('❤')
        await msg.add_reaction('💔')

        emoji = ''

        def check(reaction, user2):
            nonlocal emoji
            emoji = str(reaction.emoji)
            return user2 == member and (str(reaction.emoji) == '❤' or str(reaction.emoji) == '💔')

        try:
            reaction, user2 = await self.client.wait_for('reaction_add', timeout=60.0, check=check)
        except asyncio.TimeoutError:
            await ctx.channel.send('Timed out.')
        else:
            if emoji == '💔':
                embed = discord.Embed(
                    title = 'Yikes',
                    description = '<@' + str(member.id) + '> said no!',
                    color = discord.Color.teal()
                )
                await ctx.send(embed = embed)
                return

            confirmed = self.meta.addSoulmate(ctx.author, member)
            if not (confirmed):
                await ctx.send(embed = self.meta.embedOops())
                return

            choices = ['https://i.gifer.com/S3lf.gif',
                'https://66.media.tumblr.com/ed485a688fc03e4e8f5cdb3f4d01678b/tumblr_oyfmbl9N5W1rl58vno1_500.gif',
                'https://data.whicdn.com/images/330205015/original.gif',
                'https://66.media.tumblr.com/b46302ea92abcc8b1af97dd51f9cc434/tumblr_otrlkinIp61rdvr0eo1_500.gif',
                'https://media1.giphy.com/media/rnJuusfoWyu0U/giphy.gif',
                'https://www.alamedageek.com.br/wp-content/uploads/2017/01/upaltasaventuras.gif']

            embed = discord.Embed(
                title = 'Congratulations to the Newlyweds!',
                description = ctx.author.name + ' and ' + member.name + ' are now married!',
                color = discord.Color.teal()
            )
            embed.set_image(url = random.choice(choices))
            await ctx.send(embed = embed)

    @commands.command()
    async def divorce(self, ctx, member: discord.Member = None):
        id = ctx.author.id
        user = self.meta.getProfile(ctx.author)

        soulmates = user['soulmates']

        if len(soulmates) == 0:
            await ctx.send(embed = self.meta.embedOops())
            return

        if member is None:
            member = soulmates[0]
            member = self.client.get_user(member)
        else:
            if member.id not in soulmates:
                await ctx.send(embed = self.meta.embedOops())
                return

        spouse_name = 'soulmate'
        spouseExists = False
        if self.meta.profileDoesExist(member.id):
            spouseExists = True
            spouse_name = self.client.get_user(member.id).name

        embed = discord.Embed(
            title = 'Divorce ' + spouse_name + '?',
            description = 'React to this message with a ✅ for yes, ⛔ for no.\nYou have 60 seconds to decide!',
            color = discord.Color.teal()
        )
        await ctx.send(embed = embed)

        msg = ctx.channel.last_message
        await msg.add_reaction('✅')
        await msg.add_reaction('⛔')

        emoji = ''

        def check(reaction, user):
            nonlocal emoji
            emoji = str(reaction.emoji)
            return user == ctx.author and (str(reaction.emoji) == '✅' or str(reaction.emoji) == '⛔')

        try:
            reaction, user = await self.client.wait_for('reaction_add', timeout=60.0, check=check)
        except asyncio.TimeoutError:
            await channel.send('Timed out.')
        else:
            if emoji == '⛔':
                embed = discord.Embed(
                    title = 'Divorce canceled.',
                    color = discord.Color.teal()
                )
                await ctx.send(embed = embed)
                return

            self.meta.removeSoulmate(ctx.author, member)

            embed = discord.Embed(
                title = 'Divorced ' + spouse_name + '.',
                color = discord.Color.teal()
            )
            await ctx.send(embed = embed)
            return

def setup(client):
    database_connection = Database()
    meta_class = Meta(database_connection)
    client.add_cog(Soulmates(client, database_connection, meta_class))
