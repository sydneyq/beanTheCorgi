import discord
from discord.ext import commands

class Triggers(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def hotlines(self, ctx):
        embed = discord.Embed(
            title = 'Hotlines and Resources',
            description = '[Click here for hotlines in the USA.](https://www.dosomething.org/us/about/hotline-list)\n[Click here for a list of emergency telephone numbers for all areas.](https://en.wikipedia.org/wiki/List_of_emergency_telephone_numbers)',
            color = discord.Color.teal()
        )
        await ctx.send(embed = embed)

    @commands.Cog.listener()
    async def on_message(self, message):
        return

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        guild = self.client.get_guild(257751892241809408)
        casual = guild.get_channel(257751892241809408)
        heaven = guild.get_channel(594657206251814963)

        events = guild.get_channel(594641130545741834)
        mods = guild.get_channel(592030367796690975)
        marketing = guild.get_channel(594641226330800153)

        #angel added
        if (257755582662967305 in [role.id for role in after.roles]) and (257755582662967305 not in [role.id for role in before.roles]):
            embed = discord.Embed(
                title = after.name + ' has been given the Angel role!',
                description = '<@' + str(after.id) + '>, when you\'re able, please take a moment to check the pins of this channel and your respective team\'s channels.',
                color = discord.Color.gold()
            )

            embed.set_author(name = 'Mind Café', icon_url = 'https://cdn.discordapp.com/emojis/593214693573787654.png')
            embed.set_footer(text = 'Congratulations! 🎉')
            await heaven.send(embed = embed)
        #angel removed
        if (257755582662967305 in [role.id for role in before.roles]) and (257755582662967305 not in [role.id for role in after.roles]):
            embed = discord.Embed(
                title = after.name + ' has been removed from the Angel role.',
                color = discord.Color.gold()
            )

            await heaven.send(embed = embed)
        #mod
        if (592070664169455616 in [role.id for role in after.roles]) and (592070664169455616 not in [role.id for role in before.roles]):
            embed = discord.Embed(
                title = after.name + ' has been given the Mod role!',
                description = '<@' + str(after.id) + '>, when you\'re able, please take a moment to check the pins of this channel. Ask your teammates if you have any questions.',
                color = discord.Color.blue()
            )

            embed.set_author(name = 'Mind Café', icon_url = 'https://cdn.discordapp.com/emojis/593214693573787654.png')
            embed.set_footer(text = 'Congratulations! 🎉')
            await mods.send(embed = embed)
        #event-coord
        if (594642605862682672 in [role.id for role in after.roles]) and (594642605862682672 not in [role.id for role in before.roles]):
            embed = discord.Embed(
                title = after.name + ' has been given the Events Coordinator role!',
                description = '<@' + str(after.id) + '>, when you\'re able, please take a moment to check the pins of this channel. Ask your teammates if you have any questions.',
                color = discord.Color.red()
            )

            embed.set_author(name = 'Mind Café', icon_url = 'https://cdn.discordapp.com/emojis/593214693573787654.png')
            embed.set_footer(text = 'Congratulations! 🎉')
            await events.send(embed = embed)
        #marketing
        if (594642783160107186 in [role.id for role in after.roles]) and (594642783160107186 not in [role.id for role in before.roles]):
            embed = discord.Embed(
                title = after.name + ' has been given the Marketing Officer role!',
                description = '<@' + str(after.id) + '>, when you\'re able, please take a moment to check the pins of this channel. Ask your teammates if you have any questions.',
                color = discord.Color.green()
            )

            embed.set_author(name = 'Mind Café', icon_url = 'https://cdn.discordapp.com/emojis/593214693573787654.png')
            embed.set_footer(text = 'Congratulations! 🎉')
            await marketing.send(embed = embed)

        #certified-listener
        if (597781064718745660 in [role.id for role in after.roles]) and (597781064718745660 not in [role.id for role in before.roles]):
            embed = discord.Embed(
                title = after.name + ' is now Certified in Active Listening!',
                color = discord.Color.gold()
            )

            embed.set_author(name = 'Mind Café', icon_url = 'https://cdn.discordapp.com/emojis/594982856162541573.png')
            embed.set_footer(text = 'Congratulations! 🎉')
            await casual.send(embed = embed)
        #certification-team
        if 597801322716332044 in [role.id for role in after.roles] and 597801322716332044 not in [role.id for role in before.roles]:
            embed = discord.Embed(
                title = after.name + ' is now on the Certifying Team!',
                description = 'Thanks for helping us improve our listening quality.',
                color = discord.Color.gold()
            )

            embed.set_author(name = 'Mind Café', icon_url = 'https://cdn.discordapp.com/emojis/592850494767104011.png')
            embed.set_footer(text = 'Congratulations! 🎉')
            await casual.send(embed = embed)

def setup(client):
    client.add_cog(Triggers(client))
