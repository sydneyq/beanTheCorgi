import discord
from discord.ext import commands
import secret
import json
import os

class Help(commands.Cog):

    def __init__(self, client):
        self.client = client
        client.remove_command('help')

        dirname = os.path.dirname(__file__)
        filename2 = os.path.join(dirname, 'docs/emojis.json')
        filename3 = os.path.join(dirname, 'docs/ids.json')

        with open(filename2) as json_file:
            self.emojis = json.load(json_file)

        with open(filename3) as json_file:
            self.ids = json.load(json_file)

    @commands.command()
    async def help(self, ctx):
        embed = discord.Embed(
            title = 'Bean\'s the Name and Barkin\'s the Game',
            description = 'Created by <@' + str(secret.BOT_OWNER_ID) + '> ' + self.emojis['BotDeveloper'] + ' June 24th, 2019 for Mind Café.',
            color = discord.Color.teal()
        )
        embed.set_thumbnail(url = 'https://cdn.discordapp.com/attachments/591611902459641856/593267453363224588/Bean_Icon.png')
        embed.add_field(name = 'Help Commands',
        value = '`+funcmds` - Fun Commands List\n`+supportcmds` - Support Commands List\n`+badges` - Badges List', inline=True)

        await ctx.send(embed = embed)

    @commands.command(aliases=['commands', 'cmds', 'command', 'cmd', 'funcmd', 'fcmd', 'fcmds'])
    async def funcmds(self, ctx):
        return

    @commands.command(aliases=['supportcmd', 'supportcommands', 'scmd', 'scmds'])
    async def supportcmds(self, ctx):
        return

    @commands.command(aliases=['badgelist'])
    async def badges(self, ctx):
        return

def setup(client):
    client.add_cog(Help(client))
