import discord
from discord.ext import commands
from .meta import Meta
from database import Database
import secret
import json
import os

class Help(commands.Cog):

    def __init__(self, client, database, meta):
        self.client = client
        self.dbConnection = database
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
        embed = discord.Embed(
            title = 'Bean\'s Just For Fun Commands',
            description = '`<>` is required, `[]` is optional.',
            color = discord.Color.teal()
        )
        embed.set_thumbnail(url = 'https://cdn.discordapp.com/attachments/591611902459641856/593267453363224588/Bean_Icon.png')

        profile_commands = """`profile [@user]` - AKA `p`. Display a person's profile.
        `inventory [@user]` - AKA `i`. Display a person's inventory.
        `squads` - AKA `s`. Display the Squad leaderboard.
        `marry <@user>` - Propose to someone.
        `divorce` - Divorce your current soulmate.
        `squad <squadName>` - Join a Squad.
        `affinity <affinityType>` - Declare your affinity."""
        embed.add_field(name = 'Profile Commands', value = profile_commands)

        store_commands = """`daily` - AKA `treasurehunt`, `treasure`. Your companion finds coins daily!
        `store [c/h/i/e]` - AKA `shop`, `st`. See the store.
        `buy <item/companion>` - AKA `set`. Buy or set a Companion from the Store.
        `release` - Release your Companion.
        `gift <@user> [item/companion]` - Gift a coin gift or Companion to someone."""
        embed.add_field(name = 'Companion and Store Commands', value = store_commands)

        await ctx.send(embed = embed)
        return

    @commands.command(aliases=['supportcmd', 'supportcommands', 'scmd', 'scmds'])
    async def supportcmds(self, ctx):
        embed = discord.Embed(
            title = 'Bean\'s Support Commands',
            description = '`<>` is required, `[]` is optional.\nCommands are for Ticket Owners and Moderators+ unless specified otherwise.',
            color = discord.Color.teal()
        )
        embed.set_thumbnail(url = 'https://cdn.discordapp.com/attachments/591611902459641856/593267453363224588/Bean_Icon.png')

        support_commands = """`support [topic]` - Create a Support Ticket channel. To make a NSFW Ticket, include "nsfw" in the topic.
        `rep <@user>` - AKA `helpedby`. Give someone who's recently helped you in a Support Ticket or Support DM a Help Point. If certain conditions aren't met, the rep may be taken away. Ask a Moderator for more information.
        `archive` - Archive a Support Ticket.
        `switch` - AKA `swap`. Change a channel to NSFW or SFW. Can be used by Certifieds, the Ticket Owner, and Moderators+.
        `certified` - Only allow those Certified in Active Listening to have speech access in the Ticket.
        `lockdown` - Remove all speech access to the Ticket except for the Owner and Moderators+.
        `invite <@user>` - Invite a specific user to be able to speak in the Ticket.
        `remove <@user>` - Remove a specific user's ability to be able to speak in the Ticket.
        `reset` - Reset everyone's permissions for the Ticket."""
        embed.add_field(name = 'Support Commands', value = support_commands)

        await ctx.send(embed = embed)
        return

    @commands.command(aliases=['badgelist', 'badge'])
    async def badges(self, ctx):
        embed = discord.Embed(
            title = 'Badge List',
            description = 'These fun things can be found on your profile!',
            color = discord.Color.teal()
        )
        embed.set_thumbnail(url = 'https://cdn.discordapp.com/attachments/591611902459641856/593267453363224588/Bean_Icon.png')

        emojis = self.emojis
        position_badges = emojis['Administrator'] + ' Administrator\n' + emojis['BotDeveloper'] + ' Bot Developer\n' + emojis['Moderator'] + ' Moderator\n' + emojis['MarketingOfficer'] + ' Marketing Officer\n' + emojis['EventCoordinator'] + ' Event Coordinator\n' + emojis['CertifyingTeam'] + ' Certifying Team\n' + emojis['Certified'] + ' Certified in Active Listening\n' + emojis['Listener'] + ' Listener\n' +emojis['CorgiCallResponder'] + ' Corgi Call Responders\n'
        embed.add_field(name = 'Position Badges', value = position_badges)

        other_badges = self.dbConnection.findBadge({'id':'CaughtDitto'})['literal'] + ' - Caught the rare Ditto!\n' + self.dbConnection.findBadge({'id':'GiftedByBean'})['literal'] + ' - Gifted Bean and got a rare badge back!\n' + self.dbConnection.findBadge({'id':'2019'})['literal'] + ' - Was here in 2019 and used the 2019 badge command!\n' + self.dbConnection.findBadge({'id':'HeckinRich'})['literal'] + ' - Bought the HeckinRich badge from the Item Store!\n' + emojis['HelpPts10'] + ' - Has at least 10 Help points!\n' + emojis['Recruited10'] + ' - Has recruited at least 10 people to the server!'

        embed.add_field(name = 'Other Badges', value = other_badges)

        await ctx.send(embed = embed)
        return

def setup(client):
    database_connection = Database()
    meta_class = Meta(database_connection)
    client.add_cog(Help(client, database_connection, meta_class))
