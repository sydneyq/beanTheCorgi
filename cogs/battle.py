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

    @commands.command(aliases=['challenge'])
    async def battle(self, ctx, member: discord.Member, bet: int):
        return
        p1 = ctx.author
        p2 = member
        p1_user = self.meta.getProfile(p1)
        p2_user = self.meta.getProfile(p2)

        #check both have bet coins
        if not (p1_user['coins'] >= bet and p2_user['coins'] >= bet):
            embed = discord.Embed(
                title = 'Sorry, one of you doesn\'t have enough coins to bet that much!'
                color = discord.Color.teal()
            )
            await channel.send(embed = embed)
            return

        if p1_user['affinity'] == '' or p2_user['affinity'] == ''):
            embed = discord.Embed(
                title = 'Sorry, one of you doesn\'t have an affinity!'
                color = discord.Color.teal()
            )
            await channel.send(embed = embed)
            return

        #accept challenge?
        embed_req = discord.Embed(
            title = p2.name + ', ' + p1.name + ' challenges you to a battle! Accept?',
            description = 'React to this message with a ✅ for yes, ⛔ for no.\nYou have 60 seconds to decide!',
            color = discord.Color.teal()
        )
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
                await ctx.send(embed = embed_a)

        await self.client.send_typing(ctx.channel)
        embed = discord.Embed(
            title = 'Battle!: **' + p1.name + '** vs **' + p2.name + '**',
            color = discord.Color.teal()
        )

        p1_stats = get_battle_stats(p1_user, p1_user['affinity'])
        p2_stats = get_battle_stats(p2_user, p2_user['affinity'])

        while (p1_stats['hp'] >= 0 and p2_stats['hp'] >= 0):
            battle_turn(p2, p2_stats, p1, p1_stats)
            if (p1_stats['hp'] >= 0 and p2_stats['hp'] >= 0):
                break
            battle_turn(p1, p1_stats, p2, p2_stats)

        await asyncio.sleep(10)
        await ctx.send(embed = embed)
        #p2 wins
        if p1_hp <= 0:
            await ctx.send(embed = battle_win(p2, p2_user, p1, p1_user))
            return
        #p1 wins
        elif p2_hp <= 0:
            await ctx.send(embed = battle_win(p1, p1_user, p2, p2_user))
            return
        return

        def battle_turn(player1, p1_st, player2, p2_st):
            nonlocal embed
            battle_desc = ''

            #FLAG: not making sense because
            #for reflect and avoid to work
            #we need to be on the other person's turn
            #but for heal we need to be on ours

            #heal?
            if random.random() < p1_st['heal_chance']:
                p1_hp += p1_st['heal']
                battle_desc += p1.name + ' healed by `' + str(p1_stats['heal']) + '`!')

            #reflect?
            if random.random() < p1_st['heal_chance']:
                p1_hp += p1_st['heal']
                battle_desc += p1.name + '  by `' + str(p1_stats['heal']) + '`!')
            #elif avoid?

            #elif attacked

            embed.add_field(name=player1.name + '\'s turn!', value=battle_desc)

            nonlocal p1
            nonlocal p1_stats
            nonlocal p2
            nonlocal p2_stats
            if p1.name == player1.name:
                p1_stats = p1_st
                p2_stats = p2_st
            else:
                p1_stats = p2_st
                p2_stats = p1_st
            return

        def get_battle_stats(p_user, aff):
            #water -> chance to heal
            #air -> chance to avoid
            #earth -> higher hp
            #fire -> higher atk

            #water
            heal_chance = aff == 'Water' ? .25 : 0
            #water buff: amt healed
            heal = 10
            #earth
            #earth buff: amt more hp
            hp = aff == 'Earth' ? 150 : 100
            #air
            avoid = aff == 'Air' ? .30 : 0
            #air buff: reflect atk
            reflect = 0
            #fire
            #fire buff: amt more atk
            atk = aff == 'Fire' ? 20 : 10

            return stats = {
                "heal_chance":heal_chance,
                "heal":heal,
                "hp":hp,
                "avoid":avoid,
                "reflect":reflect,
                "atk":atk
            }

        def battle_win(p1, p1_user, p2, p2_user):
            nonlocal bet
            p1_coins = p1_user['coins'] + bet
            p2_coins = p2_user['coins'] - bet

            desc = '**' + p1.name + '\'s coins:** `' + str(p1_user['coins']) '` -> `' + str(p1_coins) '`\n'
            desc += '**' + p2.name + '\'s coins:** `' + str(p2_user['coins']) '` -> `' + str(p2_coins) '`'

            embed = discord.Embed(
                title = p1.name + ' won!',
                description = desc,
                color = discord.Color.teal()
            )

            self.dbConnection.updateProfile({"id": p1.id}, {"$set": {"coins": p1_coins}})
            self.dbConnection.updateProfile({"id": p2.id}, {"$set": {"coins": p2_coins}})
            return embed


def setup(client):
    database_connection = Database()
    meta_class = Meta(database_connection)
    client.add_cog(Battle(client, database_connection, meta_class))
