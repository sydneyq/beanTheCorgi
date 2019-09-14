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
import asyncio

class Battle(commands.Cog):

    def __init__(self, client, database, meta):
        self.client = client
        self.dbConnection = database
        self.meta = meta

    @commands.command(aliases=['card', 'bc', 'fightcard'])
    async def battlecard(self, ctx, other: discord.Member = None):
        if other == None:
            member = ctx.author
            id = ctx.author.id
        else:
            member = other
            id = other.id

        user = self.meta.getProfile(member)
        name = self.client.get_user(id).name
        aff = user['affinity']
        stats = self.get_battle_stats(user, aff)

        pic = member.avatar_url

        desc = 'Affinity: `' + aff + '` '
        if aff == 'Fire':
            desc += '(+10 ATK)'
        elif aff == 'Earth':
            desc += '(+50 HP)'
        elif aff == 'Water':
            desc += '(+20% Heal Chance)'
        elif aff == 'Air':
            desc += '(+30% Avoid Chance)'

        embed = discord.Embed(
            title = name + '\'s Battle Card',
            description = desc,
            color = discord.Color.teal()
        )

        atk = stats['atk']
        embed.add_field(name="Attack Power (ATK)", value='`' + str(atk) + '`', inline=True)

        hp = stats['hp']
        embed.add_field(name="Health (HP)", value='`' + str(hp) + '`', inline=True)

        avoid = stats['avoid_chance']
        if avoid != 0:
            embed.add_field(name="Avoidance", value='`' + str(int(avoid * 100)) + '%`', inline=True)

        #avoid = stats['reflect_chance']
        #embed.add_field(name=s"Reflection", value='`' + str(reflect) + '`', inline=True)

        heal_chance = stats['heal_chance']
        if heal_chance != 0:
            embed.add_field(name="Heal Chance", value='`' + str(int(heal_chance * 100)) + '%`', inline=True)
            heal = stats['heal']
            embed.add_field(name="Heal", value='`' + str(heal) + '`', inline=True)

        embed.set_thumbnail(url = pic)
        await ctx.send(embed = embed)

    def get_battle_stats(self, p_user, aff):
        #water -> chance to heal
        #air -> chance to avoid
        #earth -> higher hp
        #fire -> higher atk

        #water
        heal_chance = .2 if aff == 'Water' else 0
        #water buff: amt healed
        heal = 10
        #earth
        #earth buff: amt more hp
        hp = 150 if aff == 'Earth' else 100
        #air
        avoid_chance = .3 if aff == 'Air' else 0
        #air buff: reflect atk
        reflect_chance = 0
        #fire
        #fire buff: amt more atk
        atk = 30 if aff == 'Fire' else 20

        stats = {
            "heal_chance":heal_chance,
            "heal":heal,
            "hp":hp,
            "avoid_chance":avoid_chance,
            "reflect_chance":reflect_chance,
            "atk":atk
        }
        return stats

    @commands.command(aliases=['challenge'])
    async def battle(self, ctx, member: discord.Member, bet: int = 0):
        if member.bot:
            embed = discord.Embed(
                title = 'You can\'t challenge a bot!',
                color = discord.Color.teal()
            )
            await ctx.send(embed = embed)
            return

        if member == ctx.author:
            embed = discord.Embed(
                title = 'You can\'t challenge yourself!',
                color = discord.Color.teal()
            )
            await ctx.send(embed = embed)
            return

        p1 = ctx.author
        p2 = member
        p1_user = self.meta.getProfile(p1)
        p2_user = self.meta.getProfile(p2)
        reflect = False
        avoid = False

        if bet < 0:
            embed = discord.Embed(
                title = 'The bet amount has to be 0 or more!',
                color = discord.Color.teal()
            )
            await ctx.send(embed = embed)
            return

        #check both have bet coins
        if not (p1_user['coins'] >= bet and p2_user['coins'] >= bet):
            embed = discord.Embed(
                title = 'Sorry, one of you doesn\'t have enough coins to bet that much!',
                color = discord.Color.teal()
            )
            await ctx.send(embed = embed)
            return

        if p1_user['affinity'] == '' or p2_user['affinity'] == '':
            embed = discord.Embed(
                title = 'Sorry, one of you doesn\'t have an affinity!',
                color = discord.Color.teal()
            )
            await ctx.send(embed = embed)
            return

        #accept challenge?
        embed_req = discord.Embed(
            title = p2.name + ', ' + p1.name + ' challenges you to a battle for ` ' + str(bet) + ' ` coins! Accept?',
            description = 'React to this message with a ✅ for yes, ⛔ for no.\nYou have 60 seconds to decide!',
            color = discord.Color.teal()
        )
        #embed_req.set_thumbnail(url = 'https://icon-library.net/images/alert-icon/alert-icon-8.jpg')
        await ctx.send(embed = embed_req)
        msg = ctx.channel.last_message
        await msg.add_reaction('✅')
        await msg.add_reaction('⛔')
        emoji = ''
        def check(reaction, user):
            nonlocal emoji
            emoji = str(reaction.emoji)
            return user == p2 and (str(reaction.emoji) == '✅' or str(reaction.emoji) == '⛔')
        try:
            reaction, user = await self.client.wait_for('reaction_add', timeout=60.0, check=check)
        except asyncio.TimeoutError:
            await channel.send('Timed out.')
        else:
            if emoji == '⛔':
                embed_d = discord.Embed(
                    title = 'Battle request denied.',
                    color = discord.Color.teal()
                )
                await ctx.send(embed = embed_d)
                return
            else:
                embed_a = discord.Embed(
                    title = 'Challenge accepted!',
                    color = discord.Color.teal()
                )
                await ctx.send(embed = embed_a, delete_after=2)

        def battle_turn(player1, p1_st, player2, p2_st):
            nonlocal reflect
            nonlocal avoid
            battle_desc = ''

            #FLAG: not making sense because
            #for reflect and avoid to work
            #we need to be on the other person's turn
            #but for heal we need to be on ours

            #heal?
            if random.random() < p1_st['heal_chance']:
                p1_st['hp'] += p1_st['heal']
                battle_desc += '\n**' + player1.name + '** healed by `' + str(p1_st['heal']) + '`!'

            #attack
            dmg = random.randint(p1_st['atk'] - 10, p1_st['atk'])
            if reflect:
                p1_st['hp'] -= dmg
                battle_desc += '\n**' + player2.name + '** reflected `' + str(dmg) + '` damage to **' + player1.name + '**!'
            elif avoid:
                battle_desc += '\n**' + player2.name + '** avoided **' + player1.name + '**\'s attack!'
            else:
                p2_st['hp'] -= dmg
                battle_desc += '\n**' + player1.name + '** did `' + str(dmg) + '` damage to **' + player2.name + '**!'

            #reset avoid and reflect flags
            reflect = False
            avoid = False

            #reflect for next round
            if random.random() < p1_st['reflect_chance']:
                reflect = True
            #elif avoid for next round
            elif random.random() < p1_st['avoid_chance']:
                avoid = True

            nonlocal p1
            nonlocal p1_stats
            nonlocal p2
            nonlocal p2_stats
            nonlocal ctx
            nonlocal embed

            if p1.name == player1.name:
                p1_stats = p1_st
                p2_stats = p2_st
            else:
                p1_stats = p2_st
                p2_stats = p1_st

            battle_desc += '\n**' + p1.name +  '**\'s HP: `' + str(p1_stats['hp']) + '` | '
            battle_desc += '**' + p2.name +  '**\'s HP: `' + str(p2_stats['hp']) + '`'

            embed.add_field(name=player1.name + '\'s turn!', value=battle_desc, inline=False)

            #ctx.send(embed, delete_after=5)

        def battle_win(p1, p1_user, p2, p2_user):
            nonlocal bet

            if not (p1_user['coins'] >= bet and p2_user['coins'] >= bet):
                embed = discord.Embed(
                    title = p1.name + ' won!',
                    description = 'Oops, I couldn\'t change your coins! Does someone have less than the bet amount?',
                    color = discord.Color.teal()
                )
                return

            p1_coins = p1_user['coins'] + bet
            p2_coins = p2_user['coins'] - bet

            desc = '**' + p1.name + '\'s coins:** `' + str(p1_user['coins']) + '` -> `' + str(p1_coins) + '`\n'
            desc += '**' + p2.name + '\'s coins:** `' + str(p2_user['coins']) + '` -> `' + str(p2_coins) + '`'

            embed = discord.Embed(
                title = p1.name + ' won!',
                description = desc,
                color = discord.Color.teal()
            )

            embed.set_thumbnail(url = p1.avatar_url)

            self.dbConnection.updateProfile({"id": p1.id}, {"$set": {"coins": p1_coins}})
            self.dbConnection.updateProfile({"id": p2.id}, {"$set": {"coins": p2_coins}})
            return embed

        async with ctx.channel.typing():
            #embed = discord.Embed(
            #    title = 'Battle!: **' + p1.name + '** vs **' + p2.name + '**',
            #    color = discord.Color.teal()
            #)

            p1_stats = self.get_battle_stats(p1_user, p1_user['affinity'])
            p2_stats = self.get_battle_stats(p2_user, p2_user['affinity'])

            while (p1_stats['hp'] > 0 and p2_stats['hp'] > 0):
                embed = discord.Embed(
                    title = 'Battle!: **' + p1.name + '** vs **' + p2.name + '**',
                    color = discord.Color.teal()
                )
                embed.set_thumbnail(url = 'https://stardewvalleyinfo.com/wp-content/uploads/2018/01/Ancient_Sword-1-150x150.png')

                battle_turn(p2, p2_stats, p1, p1_stats)
                if (p1_stats['hp'] <= 0 or p2_stats['hp'] <= 0):
                    break
                battle_turn(p1, p1_stats, p2, p2_stats)

                await ctx.send(embed = embed, delete_after=5)
                await asyncio.sleep(6)

            #await asyncio.sleep(10)
            #await ctx.send(embed = embed)
        #p2 wins
        if p1_stats['hp'] <= 0:
            await ctx.send(embed = battle_win(p2, p2_user, p1, p1_user))
            return
        #p1 wins
        elif p2_stats['hp'] <= 0:
            await ctx.send(embed = battle_win(p1, p1_user, p2, p2_user))
            return
        return

def setup(client):
    database_connection = Database()
    meta_class = Meta(database_connection)
    client.add_cog(Battle(client, database_connection, meta_class))
