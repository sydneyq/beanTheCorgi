import discord
from discord.ext import commands
from database import Database
from .meta import Meta
import json
import os
import asyncio

class Event(commands.Cog):

    def __init__(self, client, database, meta):
        self.client = client
        self.dbConnection = database
        self.meta = meta
        
    @commands.command(aliases=['snames'])
    async def squadnames(self, ctx):
        guild = ctx.guild
        members = guild.members

        embed = discord.Embed(
            title = 'Squad Names',
            color = discord.Color.teal()
        )

        tea = 0
        teaMembers = ''
        coffee = 0
        coffeeMembers = ''

        for member in members:
            if not self.meta.isVerified(member):
                continue
            if member.nick is not None:
                if self.meta.hasWord(member.nick, 'tea'):
                    tea += 1
                    teaMembers += '<@' + str(member.id) + '>\n'
                if self.meta.hasWord(member.nick, 'coffee'):
                    coffee += 1
                    coffeeMembers += '<@' + str(member.id) + '>\n'
            else:
                if self.meta.hasWord(member.name, 'tea'):
                    tea += 1
                    teaMembers += '<@' + str(member.id) + '>\n'
                if self.meta.hasWord(member.name, 'coffee'):
                    coffee += 1
                    coffeeMembers += '<@' + str(member.id) + '>\n'

        embed.add_field(name='Members with \"tea\"', value= '`' + str(tea) + '` Members\n' + teaMembers)
        embed.add_field(name='Members with \"coffee\"', value= '`' + str(coffee) + '` Members\n' + coffeeMembers)

        await ctx.send(embed = embed)
        return

def setup(client):
    database_connection = Database()
    meta_class = Meta()
    client.add_cog(Event(client, database_connection, meta_class))
