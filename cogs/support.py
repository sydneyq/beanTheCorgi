import discord
from discord.ext import commands
from discord.utils import get

class Support(commands.Cog):

    def __init__(self, client):
        self.client = client

    #support-ticket archive channel
    @commands.command(aliases=['archiveSupport', 'archiveS'])
    async def archiveST(self, ctx):
        channel = ctx.message.channel
        guild = self.client.get_guild(257751892241809408)
        userID = int(channel.name[channel.name.rfind('-')+1:])

        if ctx.message.author.id == userID or 'Angels' in [role.name for role in ctx.message.author.roles] or 'mechanic' in [role.name for role in ctx.message.author.roles]:
            if channel.name.startswith('s-'):
                for ch in guild.text_channels:
                    if ch.name.lower() == 'log':
                        log = guild.get_channel(ch.id)
                        await log.send('Support Ticket [**' + channel.name + '**] has been archived.')
                        break

                guild = self.client.get_guild(257751892241809408) #Mind Café
                category = 0

                for c in guild.categories:
                    if c.name.lower() == 'archive':
                        category = c #Archive

                #ctx.message.channel.category = 596988830435770368
                await ctx.message.channel.edit(category = category, sync_permissions = True)
            else:
                embed = discord.Embed(
                    title = 'This doesn\'t seem to be a Support Ticket channel...',
                    color = discord.Color.teal()
                )
                await ctx.send(embed = embed)
        else:
            embed = discord.Embed(
                title = 'Sorry, you don\'t have permission to do that!',
                color = discord.Color.teal()
            )
            await ctx.send(embed = embed)

    #support-ticket close channel
    @commands.command(aliases=['closeSupport', 'closeS'])
    async def closeST(self, ctx):
        if 'Halo' in [role.name for role in ctx.message.author.roles] or 'mechanic' in [role.name for role in ctx.message.author.roles]:
            channel = ctx.message.channel
            guild = self.client.get_guild(257751892241809408)

            if channel.name.startswith('s-'):
                for ch in guild.text_channels:
                    if ch.name.lower() == 'log':
                        log = guild.get_channel(ch.id)
                        await log.send('Support Ticket [**' + channel.name + '**] has been closed.')
                        break

                await ctx.message.channel.delete(reason='Support Ticket Closed')
            else:
                embed = discord.Embed(
                    title = 'This doesn\'t seem to be a Support Ticket channel...',
                    color = discord.Color.teal()
                )
                await ctx.send(embed = embed)
        else:
            embed = discord.Embed(
                title = 'Sorry, you don\'t have permission to do that!',
                color = discord.Color.teal()
            )
            await ctx.send(embed = embed)

    #support-ticket create channel
    @commands.command()
    async def support(self, ctx, sfw = '', *, topic = ''):
        if (ctx.message.channel.name == 'support-requests'):
            channel = ctx.message.channel
            guild = self.client.get_guild(257751892241809408) #Mind Café
            category = 0
            log = 0
            message = ctx.message

            #finding log channel
            for ch in guild.text_channels:
                if ch.name.lower() == 'log':
                    log = guild.get_channel(ch.id)
                    break

            #finding support-ticket category
            for c in guild.categories:
                if c.name.lower() == 'support-tickets':
                    category = c #Support-Tickets

            #error message if no support-ticket category exists
            if category == 0 and log != 0:
                await log.send('I can\'t seem to find Support-Tickets.')
                return

            '''
            #creating the ticket
                #
            #0[name] 1[pm/channel] 2[advice?] 3[topic]
            ticket = { ctx.message.author.name }
            botmessage = 0

            embed = discord.Embed(
                title = 'Support Ticket Setup',
                description = 'Please react with one of the corresponding emojis for each option.',
                color = discord.Color.teal()
            )
                #what topic would you like support on?
            embed.add_field(name = 'I would like to be supported in...',
            value = '🌧 Depression/Anxiety\n⚠ A NSFW topic\n💕 Relationships/Friends/Family\n📋 Academics/Work/Finances\n🌽 Other')

            await ctx.send(embed = embed)

            if ('Bots' in [role.name for role in channel.last_message.author.roles]):
                botmessage = channel.last_message
                await log.send('Found support message ID: ' + str(botmessage.id))
            else:
                await log.send('Support message ID not found.')
            '''

            #if (type == None or sfw == None):
            if (sfw == ''):
                embed = discord.Embed(
                    title = 'Support Ticket Setup',
                    description = 'Please use the following command syntax:',
                    color = discord.Color.teal()
                )

                #embed.add_field(name = '+support <DM/CHANNEL> <NSFW/SFW> [SupportTopic]',
                #value = 'For example, `+support CHANNEL SFW Relationships`')

                embed.add_field(name = '+support <NSFW/SFW> [SupportTopic]',
                value = 'For example, `+support SFW Relationships`')

                await ctx.send(embed = embed)
            else:
                #if (type.toLower() == 'dm'):

                embed = discord.Embed(
                    title = 'Support Ticket Setup',
                    description = 'Gotcha! ✅',
                    color = discord.Color.teal()
                )

                await ctx.send(embed = embed)

                newChannel = await guild.create_text_channel('s-' + message.author.name + '-' + sfw + '-' + str(message.author.id), category = category)

                if (topic != ''):
                    await newChannel.edit(topic = topic)

                if (sfw.lower() == 'nsfw'):
                    await newChannel.edit(nsfw = True)
                    role = guild.get_role(257751892241809408)
                    nsfwRole = guild.get_role(445667601386045450)
                    await newChannel.set_permissions(role, read_messages=False)
                    await newChannel.set_permissions(message.author, read_messages=True)
                    await newChannel.set_permissions(nsfwRole, read_messages=True)

                await newChannel.send('__New Support Ticket created by **<@' + str(message.author.id) + '>**.__ <@&300743585584906240>')

                await log.send('New Support Ticket created by <@' + str(message.author.id) + '>. ' + '<#' + str(newChannel.id) + '>')
                if (topic != ''):
                    await newChannel.send("Topic: " + topic)

                #elif (type.toLower() == 'channel' or type.toLower() == 'c' or type.toLower() == 'public' or type.toLower() == 'chn'):


def setup(client):
    client.add_cog(Support(client))
