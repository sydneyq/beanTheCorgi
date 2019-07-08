import discord
from discord.ext import commands
from discord.utils import get

class Support(commands.Cog):

    def __init__(self, client):
        self.client = client

    #support-ticket archive channel
    @commands.command(aliases=['swapST'])
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
                await channel.edit(name = ('s-' + self.client.get_user(userID).name + '-' + 'nsfw' + '-' + str(userID)))

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
                title = 'Sorry, you don\'t have permission to do that!',
                color = discord.Color.teal()
            )
            await ctx.send(embed = embed)

    #support-ticket archive channel
    @commands.command(aliases=['archiveSupport', 'archiveS'])
    async def archiveST(self, ctx):
        channel = ctx.message.channel
        guild = self.client.get_guild(257751892241809408)
        userID = int(channel.name[channel.name.rfind('-')+1:])

        if ctx.message.author.id == userID or 'Mods' in [role.name for role in ctx.message.author.roles] or 'mechanic' in [role.name for role in ctx.message.author.roles]:
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
    async def support(self, ctx, *, topic = ''):
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

            embed = discord.Embed(
                title = 'Support Ticket Setup',
                description = 'Gotcha! ✅',
                color = discord.Color.teal()
            )

            await ctx.send(embed = embed)

            newChannel = await guild.create_text_channel('s-' + message.author.name + '-' + 'sfw' + '-' + str(message.author.id), category = category)

            if (topic != ''):
                await newChannel.edit(topic = topic)

            await newChannel.send('__New Support Ticket created by **<@' + str(message.author.id) + '>**.__ <@&300743585584906240>')

            await log.send('New Support Ticket created by <@' + str(message.author.id) + '>. ' + '<#' + str(newChannel.id) + '>')
            if (topic != ''):
                await newChannel.send("Topic: " + topic)

    #support-ticket create channel
    @commands.command()
    async def supportNSFW(self, ctx, *, topic = ''):
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

            embed = discord.Embed(
                title = 'NSFW Support Ticket Setup',
                description = 'Gotcha! ✅',
                color = discord.Color.teal()
            )

            await ctx.send(embed = embed)

            newChannel = await guild.create_text_channel('s-' + message.author.name + '-' + 'nsfw' + '-' + str(message.author.id), category = category)

            if (topic != ''):
                await newChannel.edit(topic = topic)

            await newChannel.edit(nsfw = True)
            role = guild.get_role(257751892241809408)
            spiritsRole = guild.get_role(591398086635552788)
            nsfwRole = guild.get_role(445667601386045450)
            await newChannel.set_permissions(role, read_messages=False)
            await newChannel.set_permissions(spiritsRole, read_messages=False)
            await newChannel.set_permissions(message.author, read_messages=True)
            await newChannel.set_permissions(nsfwRole, read_messages=True)

            await newChannel.send('__New NSFW Support Ticket created by **<@' + str(message.author.id) + '>**.__ <@&300743585584906240>')

            await log.send('New NSFW Support Ticket created by <@' + str(message.author.id) + '>. ' + '<#' + str(newChannel.id) + '>')
            if (topic != ''):
                await newChannel.send("Topic: " + topic)

    @commands.Cog.listener()
    async def on_message(self, message):
        if (message.channel.name == 'support' and (message.content.lower() == 'ow' or ' oww' in message.content.lower())):
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

            embed = discord.Embed(
                title = 'Support Ticket Setup',
                description = 'Gotcha! ✅',
                color = discord.Color.teal()
            )

            await message.channel.send(embed = embed)

            newChannel = await guild.create_text_channel('s-' + message.author.name + '-' + 'sfw' + '-' + str(message.author.id), category = category)

            await newChannel.send('__Hi there, **<@' + str(message.author.id) + '>**.__ I was alerted to the need for medical attention when you said, \"ow.\" \n<@&300743585584906240>')

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
