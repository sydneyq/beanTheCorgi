import discord
from discord.ext import commands
from discord.utils import get

class Support(commands.Cog):

    def __init__(self, client):
        self.client = client

    #support-ticket reset
    @commands.command(aliases=['Reset', 'resetST'])
    async def reset(self, ctx):
        channel = ctx.message.channel
        guild = self.client.get_guild(257751892241809408)
        userID = int(channel.name[channel.name.rfind('-')+1:])

        if ctx.message.author.id == userID or 'Mods' in [role.name for role in ctx.message.author.roles] or 'mechanic' in [role.name for role in ctx.message.author.roles]:
            if channel.name.startswith('s-'):
                channel = ctx.message.channel
                guild = self.client.get_guild(257751892241809408) #Mind Café
                userID = int(channel.name[channel.name.rfind('-')+1:])
                category = 0
                log = 0
                message = ctx.message

                #finding log channel
                for ch in guild.text_channels:
                    if ch.name.lower() == 'log':
                        log = guild.get_channel(ch.id)
                        break

                await channel.edit(sync_permissions = True)

                embed = discord.Embed(
                    title = 'Channel reset! ✅',
                    color = discord.Color.teal()
                )
                await ctx.send(embed = embed)
            else:
                embed = discord.Embed(
                    title = 'This doesn\'t seem to be a Support Ticket channel...',
                    color = discord.Color.teal()
                )
                await ctx.send(embed = embed)
        else:
            embed = discord.Embed(
                title = 'Sorry, only the Support Ticket Owner and Moderators+ are able to use that command.',
                color = discord.Color.teal()
            )
            await ctx.send(embed = embed)

    #support-ticket certified only
    @commands.command(aliases=['Remove', 'deny', 'Deny'])
    async def remove(self, ctx, member: discord.Member = None):
        channel = ctx.message.channel
        guild = self.client.get_guild(257751892241809408)
        userID = int(channel.name[channel.name.rfind('-')+1:])

        if ctx.message.author.id == userID or 'Mods' in [role.name for role in ctx.message.author.roles] or 'mechanic' in [role.name for role in ctx.message.author.roles]:
            if channel.name.startswith('s-'):
                channel = ctx.message.channel
                guild = self.client.get_guild(257751892241809408) #Mind Café
                userID = int(channel.name[channel.name.rfind('-')+1:])
                category = 0
                log = 0
                message = ctx.message

                #finding log channel
                for ch in guild.text_channels:
                    if ch.name.lower() == 'log':
                        log = guild.get_channel(ch.id)
                        break

                newChannel = channel

                if (member != None):
                    await newChannel.set_permissions(member, send_messages=False)

                    embed = discord.Embed(
                        title = 'Removed ' + str(member.name) + '! ✅',
                        color = discord.Color.teal()
                    )
                    await ctx.send(embed = embed)
                else:
                    embed = discord.Embed(
                        title = 'Please pass in a member you\'d like to remove.',
                        color = discord.Color.teal()
                    )
                    await ctx.send(embed = embed)
            else:
                embed = discord.Embed(
                    title = 'This doesn\'t seem to be a Support Ticket channel...',
                    color = discord.Color.teal()
                )
                await ctx.send(embed = embed)
        else:
            embed = discord.Embed(
                title = 'Sorry, only the Support Ticket Owner and Moderators+ are able to use that command.',
                color = discord.Color.teal()
            )
            await ctx.send(embed = embed)

    #support-ticket certified only
    @commands.command(aliases=['Add', 'invite', 'Invite'])
    async def add(self, ctx, member: discord.Member = None):
        channel = ctx.message.channel
        guild = self.client.get_guild(257751892241809408)
        userID = int(channel.name[channel.name.rfind('-')+1:])

        if ctx.message.author.id == userID or 'Mods' in [role.name for role in ctx.message.author.roles] or 'mechanic' in [role.name for role in ctx.message.author.roles]:
            if channel.name.startswith('s-'):
                channel = ctx.message.channel
                guild = self.client.get_guild(257751892241809408) #Mind Café
                userID = int(channel.name[channel.name.rfind('-')+1:])
                category = 0
                log = 0
                message = ctx.message

                #finding log channel
                for ch in guild.text_channels:
                    if ch.name.lower() == 'log':
                        log = guild.get_channel(ch.id)
                        break

                newChannel = channel

                if (member != None):
                    await newChannel.set_permissions(member, read_messages=True, send_messages=True)

                    embed = discord.Embed(
                        title = 'Added ' + str(member.name) + '! ✅',
                        color = discord.Color.teal()
                    )
                    await ctx.send(embed = embed)
                else:
                    embed = discord.Embed(
                        title = 'Please pass in a member you\'d like to invite.',
                        color = discord.Color.teal()
                    )
                    await ctx.send(embed = embed)
            else:
                embed = discord.Embed(
                    title = 'This doesn\'t seem to be a Support Ticket channel...',
                    color = discord.Color.teal()
                )
                await ctx.send(embed = embed)
        else:
            embed = discord.Embed(
                title = 'Sorry, only the Support Ticket Owner and Moderators+ are able to use that command.',
                color = discord.Color.teal()
            )
            await ctx.send(embed = embed)

    #support-ticket lockdown
    @commands.command(aliases=['Lock', 'lockdown', 'Lockdown', 'lockST', 'lockdownST'])
    async def lock(self, ctx):
        channel = ctx.message.channel
        guild = self.client.get_guild(257751892241809408)
        userID = int(channel.name[channel.name.rfind('-')+1:])

        if ctx.message.author.id == userID or 'Mods' in [role.name for role in ctx.message.author.roles] or 'mechanic' in [role.name for role in ctx.message.author.roles]:
            if channel.name.startswith('s-'):
                channel = ctx.message.channel
                guild = self.client.get_guild(257751892241809408) #Mind Café
                userID = int(channel.name[channel.name.rfind('-')+1:])
                category = 0
                log = 0
                message = ctx.message

                #finding log channel
                for ch in guild.text_channels:
                    if ch.name.lower() == 'log':
                        log = guild.get_channel(ch.id)
                        break

                newChannel = channel

                role = guild.get_role(257751892241809408)
                spiritsRole = guild.get_role(591398086635552788)
                certifiedRole = guild.get_role(597781064718745660)
                modRole = guild.get_role(592070664169455616)
                await newChannel.set_permissions(role, read_messages=False)
                await newChannel.set_permissions(spiritsRole, read_messages=True, send_messages=False)
                await newChannel.set_permissions(self.client.get_user(userID), read_messages=True, send_messages=True)
                await newChannel.set_permissions(certifiedRole, read_messages=True, send_messages=False)
                await newChannel.set_permissions(modRole, read_messages=True, send_messages=True)

                await log.send('<@' + str(message.author.id) + '> has switched ' + '<#' + str(newChannel.id) + '> to Lockdown.')

                embed = discord.Embed(
                    title = 'Channel is on Lockdown! ✅',
                    color = discord.Color.teal()
                )
                await ctx.send(embed = embed)
            else:
                embed = discord.Embed(
                    title = 'This doesn\'t seem to be a Support Ticket channel...',
                    color = discord.Color.teal()
                )
                await ctx.send(embed = embed)
        else:
            embed = discord.Embed(
                title = 'Sorry, only the Support Ticket Owner and Moderators+ are able to use that command.',
                color = discord.Color.teal()
            )
            await ctx.send(embed = embed)

    #support-ticket certified only
    @commands.command(aliases=['Certified', 'certifiedST'])
    async def certified(self, ctx):
        channel = ctx.message.channel
        guild = self.client.get_guild(257751892241809408)
        userID = int(channel.name[channel.name.rfind('-')+1:])

        if ctx.message.author.id == userID or 'Mods' in [role.name for role in ctx.message.author.roles] or 'mechanic' in [role.name for role in ctx.message.author.roles]:
            if channel.name.startswith('s-'):
                channel = ctx.message.channel
                guild = self.client.get_guild(257751892241809408) #Mind Café
                userID = int(channel.name[channel.name.rfind('-')+1:])
                category = 0
                log = 0
                message = ctx.message

                #finding log channel
                for ch in guild.text_channels:
                    if ch.name.lower() == 'log':
                        log = guild.get_channel(ch.id)
                        break

                newChannel = channel

                role = guild.get_role(257751892241809408)
                spiritsRole = guild.get_role(591398086635552788)
                certifiedRole = guild.get_role(597781064718745660)
                modRole = guild.get_role(592070664169455616)
                await newChannel.set_permissions(role, read_messages=False)
                await newChannel.set_permissions(spiritsRole, read_messages=True, send_messages=False)
                await newChannel.set_permissions(self.client.get_user(userID), read_messages=True, send_messages=True)
                await newChannel.set_permissions(certifiedRole, read_messages=True, send_messages=True)
                await newChannel.set_permissions(modRole, read_messages=True, send_messages=True)

                await log.send('<@' + str(message.author.id) + '> has switched ' + '<#' + str(newChannel.id) + '> to Certified.')

                embed = discord.Embed(
                    title = 'Channel is now Certified-only! ✅',
                    color = discord.Color.teal()
                )
                await ctx.send(embed = embed)
            else:
                embed = discord.Embed(
                    title = 'This doesn\'t seem to be a Support Ticket channel...',
                    color = discord.Color.teal()
                )
                await ctx.send(embed = embed)
        else:
            embed = discord.Embed(
                title = 'Sorry, only the Support Ticket Owner and Moderators+ are able to use that command.',
                color = discord.Color.teal()
            )
            await ctx.send(embed = embed)

    #support-ticket switch channel
    @commands.command(aliases=['swapST', 'swap', 'swapst', 'SwapST', 'switch', 'switchst'])
    async def switchST(self, ctx):
        channel = ctx.message.channel
        guild = self.client.get_guild(257751892241809408)
        userID = int(channel.name[channel.name.rfind('-')+1:])

        if ctx.message.author.id == userID or 'Mods' in [role.name for role in ctx.message.author.roles] or 'mechanic' in [role.name for role in ctx.message.author.roles]:
            if channel.name.startswith('s-'):
                channel = ctx.message.channel
                guild = self.client.get_guild(257751892241809408) #Mind Café
                userID = int(channel.name[channel.name.rfind('-')+1:])
                category = 0
                log = 0
                message = ctx.message

                #finding log channel
                for ch in guild.text_channels:
                    if ch.name.lower() == 'log':
                        log = guild.get_channel(ch.id)
                        break

                newChannel = channel
                #await channel.edit(name = ('s-' + self.client.get_user(userID).name + '-' + 'nsfw' + '-' + str(userID)))

                await newChannel.edit(nsfw = True)
                role = guild.get_role(257751892241809408)
                spiritsRole = guild.get_role(591398086635552788)
                nsfwRole = guild.get_role(445667601386045450)
                await newChannel.set_permissions(role, read_messages=False)
                await newChannel.set_permissions(spiritsRole, read_messages=False)
                await newChannel.set_permissions(self.client.get_user(userID), read_messages=True)
                await newChannel.set_permissions(nsfwRole, read_messages=True)

                await log.send('<@' + str(message.author.id) + '> has switched ' + '<#' + str(newChannel.id) + '> to NSFW.')

                embed = discord.Embed(
                    title = 'Switched support channel to NSFW! ✅',
                    color = discord.Color.teal()
                )
                await ctx.send(embed = embed)
            else:
                embed = discord.Embed(
                    title = 'This doesn\'t seem to be a Support Ticket channel...',
                    color = discord.Color.teal()
                )
                await ctx.send(embed = embed)
        else:
            embed = discord.Embed(
                title = 'Sorry, only the Support Ticket Owner and Moderators+ are able to use that command.',
                color = discord.Color.teal()
            )
            await ctx.send(embed = embed)

    #support-ticket archive channel
    @commands.command(aliases=['archiveSupport', 'archiveS', 'archivest', 'archive'])
    async def archiveST(self, ctx):
        channel = ctx.message.channel
        guild = self.client.get_guild(257751892241809408)
        userID = int(channel.name[channel.name.rfind('-')+1:])

        if ctx.message.author.id == userID or 'Mods' in [role.name for role in ctx.message.author.roles] or 'mechanic' in [role.name for role in ctx.message.author.roles]:
            if channel.name.startswith('s-') or channel.name.startswith('mm-'):
                for ch in guild.text_channels:
                    if ch.name.lower() == 'log':
                        log = guild.get_channel(ch.id)
                        await log.send('Support Ticket or ModMail Ticket [**' + channel.name + '**] has been archived.')
                        break

                guild = self.client.get_guild(257751892241809408) #Mind Café
                category = 0

                for c in guild.categories:
                    if c.name.lower() == 'archive':
                        category = c #Archive

                if channel.name.startswith('s-'):
                    user = discord.utils.get(self.client.get_all_members(), id=userID)

                    embed = discord.Embed(
                        title = 'Thanks for talking with us!',
                        description = 'If you felt a Listener was supportive, you can use the command `+helpedby @user` in #botspam to show them how much you appreciated their help!',
                        color = discord.Color.teal()
                    )
                    embed.set_thumbnail(url = 'https://cdn.discordapp.com/emojis/602887275289772052.png?v=1')

                    try:
                        await user.send(embed = embed)
                    except:
                        print('Could not send private message.')

                await ctx.message.channel.edit(name = 'archived-'+ self.client.get_user(userID).name)
                #ctx.message.channel.category = 596988830435770368
                await ctx.message.channel.edit(category = category, sync_permissions = True)
            else:
                embed = discord.Embed(
                    title = 'This doesn\'t seem to be a Support/ModMail Ticket channel...',
                    color = discord.Color.teal()
                )
                await ctx.send(embed = embed)
        else:
            embed = discord.Embed(
                title = 'Sorry, only the Support Ticket Owner and Moderators+ are able to use that command.',
                color = discord.Color.teal()
            )
            await ctx.send(embed = embed)

    #support-ticket close channel
    @commands.command(aliases=['closeSupport', 'closeS', 'close', 'closest'])
    async def closeST(self, ctx):
        if 'Halo' in [role.name for role in ctx.message.author.roles] or 'mechanic' in [role.name for role in ctx.message.author.roles]:
            channel = ctx.message.channel
            guild = self.client.get_guild(257751892241809408)

            if channel.name.startswith('s-') or channel.name.startswith('mm-') or channel.name.startswith('archived-'):
                await ctx.message.channel.delete(reason='Support Ticket Closed')
            else:
                embed = discord.Embed(
                    title = 'This doesn\'t seem to be a Support/ModMail Ticket channel...',
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
    async def support(self, ctx, *, topic = ''):
        if (594008586779361311 in [role.id for role in ctx.message.author.roles]):
            embed = discord.Embed(
                title = 'Sorry, those with the Blindfolded role are not able to create support channels.',
                color = discord.Color.teal()
            )
            await ctx.send(embed = embed)
            return

        if (ctx.message.channel.name == 'support'):
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

            newChannel = await guild.create_text_channel('s-' + message.author.name + '-' + str(message.author.id), category = category)

            embed = discord.Embed(
                title = 'Support Ticket Setup',
                description = 'Gotcha! ✅\n<#' + str(newChannel.id) + '>',
                color = discord.Color.teal()
            )

            await ctx.send(embed = embed)

            if (topic != ''):
                await newChannel.edit(topic = topic)

            if ('nsfw' in topic.lower()):
                await newChannel.edit(nsfw = True)
                role = guild.get_role(257751892241809408)
                spiritsRole = guild.get_role(591398086635552788)
                nsfwRole = guild.get_role(445667601386045450)
                await newChannel.set_permissions(role, read_messages=False)
                await newChannel.set_permissions(spiritsRole, read_messages=False)
                await newChannel.set_permissions(message.author, read_messages=True)
                await newChannel.set_permissions(nsfwRole, read_messages=True)

            if ('test' not in topic.lower()):
                await newChannel.send('__New Support Ticket created by **<@' + str(message.author.id) + '>**.__ <@&300743585584906240>')

            embed2 = discord.Embed(
                title = 'Support Ticket Help',
                description = 'Only Support Ticket Owners and Moderators+ may use commands.',
                color = discord.Color.teal()
            )

            embed2.add_field(name = 'Control Commands',
            value = '`+archive`\t\tArchive this channel when finished\n`+switch`\t\tChange this channel to NSFW')

            embed2.add_field(name = 'Access Commands',
            value = '`+certified`\t\tMake the channel accessible to only Certifieds\n`+lockdown`\t\tRemove all public access to type in the channel\n`+invite <@user>`\t\tAllow a specific person to type in the channel\n`+remove <@user>`\t\tDisallow a specific person to type in the channel\n`+reset`\t\tReset the channel to default access')

            embed2.add_field(name = 'Help Repping',
            value = 'Want to thank someone for supporting you? `+helpedby @user` gives them a Help point!')

            await newChannel.send(embed = embed2)

            await log.send('New Support Ticket created by <@' + str(message.author.id) + '>. ' + '<#' + str(newChannel.id) + '>')
            if (topic != ''):
                await newChannel.send("Topic: " + topic)

    @commands.Cog.listener()
    async def on_message(self, message):
        if (message.channel.name == 'support' and (message.content.lower() == 'ow' or ' oww' in message.content.lower())):

            if (594008586779361311 in [role.id for role in message.author.roles]):
                embed = discord.Embed(
                    title = 'Sorry, those with the Blindfolded role are not able to create support channels.',
                    color = discord.Color.teal()
                )
                await message.channel.send(embed = embed)
                return

            channel = message.channel
            guild = self.client.get_guild(257751892241809408) #Mind Café
            category = 0
            log = 0

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

            newChannel = await guild.create_text_channel('s-' + message.author.name + '-' + 'sfw' + '-' + str(message.author.id), category = category)

            embed = discord.Embed(
                title = 'Support Ticket Setup',
                description = 'Gotcha! ✅\n<#' + str(newChannel.id) + '>',
                color = discord.Color.teal()
            )

            await message.channel.send(embed = embed)

            await newChannel.send('__Hi there, **<@' + str(message.author.id) + '>**.__ I was alerted to the need for medical attention when you said, \"ow.\" \n<@&300743585584906240>')

            embed2 = discord.Embed(
                title = 'Support Ticket Help',
                description = 'Only Support Ticket Owners and Moderators+ may use commands.',
                color = discord.Color.teal()
            )

            embed2.add_field(name = 'Control Commands',
            value = '`+archive`\t\tArchive this channel when finished\n`+switch`\t\tChange this channel to NSFW')

            embed2.add_field(name = 'Access Commands',
            value = '`+certified`\t\tMake the channel accessible to only Certifieds\n`+lockdown`\t\tRemove all public access to type in the channel\n`+invite <@user>`\t\tAllow a specific person to type in the channel\n`+remove <@user>`\t\tDisallow a specific person to type in the channel\n`+reset`\t\tReset the channel to default access')

            await newChannel.send(embed = embed2)

            await log.send('New Support Ticket created by <@' + str(message.author.id) + '>. ' + '<#' + str(newChannel.id) + '>')

        #I am satisfied with my care
        elif ('i am satisfied with my care' in message.content.lower() or 'i\'m satisfied with my care' in message.content.lower()):
            guild = self.client.get_guild(257751892241809408)
            channel = message.channel

            if channel.name.startswith('s-'):
                userID = int(channel.name[channel.name.rfind('-')+1:])
                if (userID == message.author.id):
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
                    await message.channel.edit(category = category, sync_permissions = True)
                else:
                    embed = discord.Embed(
                        title = 'Sorry, you don\'t have permission to do that!',
                        color = discord.Color.teal()
                    )
                    await ctx.send(embed = embed)
            else:
                embed = discord.Embed(
                    title = 'This doesn\'t seem to be a Support Ticket channel...',
                    color = discord.Color.teal()
                )
                await ctx.send(embed = embed)

def setup(client):
    client.add_cog(Support(client))
