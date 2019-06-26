import discord
from discord.ext import commands
from discord.utils import get

class Support(commands.Cog):

    def __init__(self, client):
        self.client = client

    #support-ticket close channel
    @commands.command(aliases=['closeSupport', 'closeST', 'close'])
    async def closeTicket(self, ctx):
        if 'mods' in [role.name for role in ctx.message.author.roles] or 'mechanic' in [role.name for role in ctx.message.author.roles]:
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
    async def support(self, ctx):
        if (ctx.message.channel.name == 'cmd'):
            channel = ctx.message.channel
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

            if ('Bean the Corgi' in [role.name for role in channel.last_message.author.roles]):
                await log.send('Found support message ID.')
                botmessage = channel.last_message
            else:
                await log.send('Support message ID not found.')

            await log.send('Entering emoji loop.')
            for emoji in discord.Client.emojis:
                if emoji.name == '{Warning}':
                    await log.send('Found emoji.')
                    await botmessage.add_reaction(emoji)

            '''
            emoji = discord.utils.get(discord.Client.get_all_emojis(), id=469334117020991508)
            #get(ctx.get_all_emojis(), name='🌧')
            await message.add_reaction(message, emoji)
            emoji = get(self.client.get_all_emojis(), name='⚠')
            await message.add_reaction(message, emoji)
            emoji = get(self.client.get_all_emojis(), name='💕')
            await message.add_reaction(message, emoji)
            emoji = get(self.client.get_all_emojis(), name='📋')
            await message.add_reaction(message, emoji)
            emoji = get(self.client.get_all_emojis(), name='🌽')
            await message.add_reaction(message, emoji)
            '''
            #while True:
            #reaction = await bot.wait_for_reaction(emoji=['🌧','⛔','💕','💵','🍵'], message=message)

            #PM


            '''
                #pm/public
            embed.add_field(name = 'I would like to be supported in...',
            value = '🤝 Private messages with a listener\n👑 A public support channel')

            await ctx.send(embed = embed)
            if ('Bean the Corgi' in [role.name for role in channel.last_message.author]):
                message = channel.last_message
                emoji = get(self.client.get_all_emojis(), name='🤝')
                await message.add_reaction(message, emoji)
                emoji = get(self.client.get_all_emojis(), name='👑')
                await message.add_reaction(message, emoji)
                while True:
                reaction = await bot.wait_for_reaction(emoji=['🤝','👑'], message=message)
                #PM
                if (reaction.emoji == '🤝'):

            '''


            #logging a support channel being made
            if log != 0:
                #newChannelName = 's-' + message.author.name
                #newChannel = await guild.create_text_channel(newChannelName, category = category)
                #await newChannel.send('')
                await log.send('Support Ticket for [**' + ctx.message.author.name + '**] has been created.')


def setup(client):
    client.add_cog(Support(client))
