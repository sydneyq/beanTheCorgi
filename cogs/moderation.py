import discord
from discord.ext import commands
from database import Database
from .meta import Meta
import random
import pymongo
from bson import objectid

class Moderation(commands.Cog):

    def __init__(self, client, database, meta):
        self.client = client
        self.dbConnection = database
        self.meta = meta

        dirname = os.path.dirname(__file__)
        filename = os.path.join(dirname, 'docs/rules.json')
        filename2 = os.path.join(dirname, 'docs/emojis.json')
        filename3 = os.path.join(dirname, 'docs/ids.json')

        with open(filename) as json_file:
            self.rules = json.load(json_file)

        with open(filename2) as json_file:
            self.emojis = json.load(json_file)

        with open(filename3) as json_file:
            self.ids = json.load(json_file)

    def getModLogs(self, member: discord.Member):
        return self.dbConnection.findModLogs({'id' : member.id})

    def getModProfile(self, member: discord.Member):
        return self.dbConnection.findModProfile({'id' : member.id})

    def modProfileExists(self, id):
        profile = self.dbConnection.findModProfile({"id": id})
        if profile is None:
            return False
        else:
            return True

    def getModProfile(self, member: discord.Member):
        if member is None:
            return

        id = member.id

        profile = self.dbConnection.findModProfile({"id": id})
        if profile is None:
            self.dbConnection.insertModProfile({'id': id, 'strikes':0})
            profile = self.dbConnection.findModProfile({"id": id})

        return profile

    def checkStrikes(self, member: discord.Member):
        profile = self.getModProfile(member)
        strikes = profile['strikes']

        if strikes >= 10:
            self.ban(member)
            return 'The member was permabanned.'
        elif strikes >= 9:
            self.blindfold(member)
            return 'The member was Blindfolded.'
        elif strikes >= 7:
            self.mute(member, 72)
            return 'The member was muted for 72h.'
        elif strikes >= 5:
            self.mute(member, 24)
            return 'The member was muted for 24h.'
        elif strikes >= 3:
            self.mute(member, 6)
            return 'The member was muted for 6h.'

    def embedMuted(self, hours: int = -1):
        title = 'You have been muted'
        if hours != -1:
            title += 'for `'+str(hours)+'` hours'
        embed = discord.Embed(
            title = title,
            color = discord.Color.red()
        )
        return embed

    def embedBanned(self):
        embed = discord.Embed(
            title = 'You have been banned from Mind Café',
            color = discord.Color.red()
        )
        return embed

    def embedBlindfolded(self):
        embed = discord.Embed(
            title = 'You have been blindfolded',
            description = 'You no longer have access to casual channels and may only receive support through requesting support DMs'
            color = discord.Color.red()
        )
        return embed

    def embedUnmuted(self):
        embed = discord.Embed(
            title = 'You have been unmuted',
            color = discord.Color.red()
        )
        return embed

    def embedUnblindfolded(self):
        embed = discord.Embed(
            title = 'You have been unblindfolded',
            color = discord.Color.red()
        )
        return embed

    async def ban(self, user: discord.User):
        await ban(user)
        try:
            await member.send(embed = self.embedBanned())
        return

    async def unban(self, user: discord.User):
        await unban(user)
        return

    async def mute(self, member: discord.Member, hrs: int = -1):
        muted = guild.get_role(445398365606248448)
        await member.add_roles(muted)
        try:
            await member.send(embed = self.embedMuted(hrs))
        return

    async def unmute(self, member: discord.Member):
        muted = guild.get_role(445398365606248448)
        await member.remove_roles(muted)
        try:
            await member.send(embed = self.embedUnmuted())
        return

    async def blindfold(self, member: discord.Member):
        role = guild.get_role(self.ids['BLINDFOLDED_ROLE'])
        await member.add_roles(role)
        try:
            await member.send(embed = self.embedBlindfolded())
        return

    async def unblindfold(self, member: discord.Member):
        role = guild.get_role(self.ids['BLINDFOLDED_ROLE'])
        await member.remove_roles(role)
        try:
            await member.send(embed = self.embedUnblindfolded())
        return

    def changeStrikes(self, member:discord.Member, strikes:int):
        if not self.modProfileExists(member.id):
            return False
        self.dbConnection.updateProfile({"id": member.id}, {"$set": {"strikes": strikes}})
        return True

    def getRuleJSON(rule: int):
        rule_json = self.rules[rule]
        return rule_json

    def getAmtStrikesFromRule(self, rule: int):
        rule_json = self.getRuleJSON(rule)
        return int(rule_json['STRIKES'])

    @commands.command(aliases=['warn', 'sanction'])
    async def strike(self, ctx, member: discord.Member, rule:int, *, reason = None):
        if not self.meta.isMod(ctx.author):
            await ctx.send(embed = self.meta.embedOops()
            return
        elif member.bot: #or self.isAdmin(member):
            await ctx.send(embed = self.meta.embedOops()
            return
        if rule < 0 or rule > 14:
            await ctx.send(embed = self.meta.embedOops()
            return

        if reason is None:
            reason = 'No reason provided'

        profile = self.getModProfile(member)
        before_strikes = profile['strikes']
        after_strikes = profile['strikes'] + self.getAmtStrikesFromRule(rule)
        self.dbConnection.insertModLog({'id': member.id, 'rule': rule, 'reason': reason, 'staff': ctx.author.id, 'date': self.meta.getFullDateTime()})

        try:
            embed = discord.Embed(
                title = 'Consider it done! ✅',
                color = discord.Color.red()
            )
            n = 'You\'ve been striked for: Rule `'+str(rule)+'`'
            v = 'Strikes: `'+str(before_strikes)+'->'+str(after_strikes)+'`
            embed.add_field(name=n, value=v)
            n = 'Rule `'+str(rule)+'` description'
            v = self.getRuleJSON['DESC']
            embed.add_field(name=n, value=v)
            n = 'Moderator\'s custom message'
            v = reason
            embed.add_field(name=n, value=v)
            await member.send(embed = embed)

        action = 'No further action was taken.'
        if not (before_strikes == after_strikes):
            action = self.checkStrikes(member)

        embed = discord.Embed(
            title = 'Consider it done! ✅',
            color = discord.Color.red()
        )
        n = member.name + ' has been striked. `['+ str(before_strikes) + '->' + str(after_strikes)+']`'
        v = 'Rule `'+str(rule)+'`: ```' + reason + '```'
        embed.add_field(name=n, value=v)
        embed.set_footer(text = action)
        await ctx.send(embed = embed)

    @commands.command(aliases=['deletestrike', 'delstrike'])
    async def removestrike(self, ctx, strikeID: objectid.ObjectId = None):
        if not self.meta.isMod(ctx.author):
            await ctx.send(embed = self.meta.embedOops())
            return

        if strikeID is None:
            embed = discord.Embed(
                description = 'Correct Usage: `+removestrike strikeID`.',
                color = discord.Color.teal()
            )
            await ctx.send(embed = embed)
            return

        modlog = self.dbConnection.findModLog({'_id' : strikeID})
        if modlog is None:
            await ctx.send(embed = self.meta.embedOops())
            return

        member = self.client.get_user(modlog['id'])
        profile = self.getModProfile(member)
        before_strikes = profile['strikes']
        after_strikes = before_strikes - self.getAmtStrikesFromRule(modlog['rule'])
        self.changeStrikes(member, strikes)

        self.dbConnection.removeModLog({'_id' : strikeID})

        embed = discord.Embed(
            title = 'Consider it done! ✅',
            description = member.name '\'s Strikes: `'+str(before_strikes)+'->'+str(after_strikes)+'`',
            color = discord.Color.red()
        )
        await ctx.send(embed = embed)

    @commands.command(aliases=['mp', 'modlog', 'ml', 'log', 'strikes'])
    async def modprofile(self, ctx, member: discord.Member = None):
        channel = ctx.channel
        #must be by mod
        if not self.meta.isMod(ctx.author):
            if member is None:
                channel = ctx.author
            else:
                await ctx.send(self.meta.embedOops())
                return
        #for non-admins, must be in modlog channel
        elif not self.meta.isAdmin(ctx.author):
            if ctx.channel.id != 367863780627185685:
                await ctx.send(self.meta.embedOops())
                return

        if member is None:
            member = ctx.author

        logs = self.getModLogs(member)
        numLogs = logs.count()
        #they have no logs
        if not self.modProfileExists(member.id) or numLogs == 0:
            embed = discord.Embed(
                title = member.name + ' has no logs.',
                color = discord.Color.teal()
            )
            try:
                await channel.send(embed = embed)
            except:
                await ctx.send(embed = self.meta.embedOops())
            return

        profile = self.getModProfile(member)

        title = member.name + '\'s Log'
        desc += 'Total Strikes: `' + str(profile['strikes']) + '`'
        desc += '\nNumber of Logs: `' + str(numLogs) + '`'
        embed.add_field(name=title,value=desc)

        embed = discord.Embed(
            title = title,
            description = desc,
            color = discord.Color.red()
        )

        for doc in logs:
            n = 'Rule `' +doc['rule']+ '` by <@' + str(doc['staff']) + '>'
            v = '`'+str(doc['date'])+'`: ' + doc['_id']
            embed.add_field(name=n, value=v)

        pic = member.avatar_url
        embed.set_thumbnail(url = pic)

        try:
            await channel.send(embed = embed)
        except:
            await ctx.send(embed = self.meta.embedOops())
        return

    @commands.command(aliases=['strikehelp', 'modsystem'])
    async def strikesystem(self, ctx):
        embed = discord.Embed(
            title = 'Moderation Strike System',
            description = 'See the spreadsheet here: (https://docs.google.com/spreadsheets/d/1t3ppHecBITclZdoQ7t-VQMdBHsQ_-5tepOvdw3qLQlU)[https://docs.google.com/spreadsheets/d/1t3ppHecBITclZdoQ7t-VQMdBHsQ_-5tepOvdw3qLQlU]',
            color = discord.Color.red()
        )
        await ctx.send(embed = embed)
        return

def setup(client):
    database_connection = Database()
    meta_class = Meta(database_connection)
    client.add_cog(Moderation(client, database_connection, meta_class))
