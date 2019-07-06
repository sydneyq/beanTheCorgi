import discord
from discord.ext import commands

class ModMail(commands.Cog):

    def __init__(self, client):
        self.client = client

    #modmail archive channel
    @commands.command()
    async def archiveMM(self, ctx):
        if 'Angels' in [role.name for role in ctx.message.author.roles] or 'mechanic' in [role.name for role in ctx.message.author.roles]:
            channel = ctx.message.channel
            if channel.name.startswith('mm-'):
                guild = self.client.get_guild(257751892241809408) #Mind Café
                category = 0

                for c in guild.categories:
                    if c.name.lower() == 'archive':
                        category = c #Archive

                #ctx.message.channel.category = 596988830435770368
                await ctx.message.channel.edit(category = category, sync_permissions = True)
            else:
                embed = discord.Embed(
                    title = 'This doesn\'t seem to be a ModMail channel...',
                    color = discord.Color.teal()
                )
                await ctx.send(embed = embed)
        else:
            embed = discord.Embed(
                title = 'Sorry, you don\'t have permission to do that!',
                color = discord.Color.teal()
            )
            await ctx.send(embed = embed)

    #modmail close channel
    @commands.command()
    async def closeMM(self, ctx):
        if 'Halo' in [role.name for role in ctx.message.author.roles] or 'mechanic' in [role.name for role in ctx.message.author.roles]:
            channel = ctx.message.channel
            if channel.name.startswith('mm-'):
                await ctx.message.channel.delete(reason='ModMail Ticket Closed')
            else:
                embed = discord.Embed(
                    title = 'This doesn\'t seem to be a ModMail channel...',
                    color = discord.Color.teal()
                )
                await ctx.send(embed = embed)
        else:
            embed = discord.Embed(
                title = 'Sorry, you don\'t have permission to do that!',
                color = discord.Color.teal()
            )
            await ctx.send(embed = embed)

    #modmail DM listener
    @commands.Cog.listener()
    async def on_message(self, message):
        #the bot itself
        if (message.author.id == 592436047175221259 or message.author.id == 432038389663924225):
            return

        if isinstance(message.channel, discord.DMChannel):
            #check if Modmail category has a channel of them already
            guild = self.client.get_guild(257751892241809408) #Mind Café
            category = 0

            for c in guild.categories:
                if c.name.lower() == 'modmail':
                    category = c #ModMail

            if category == 0:
                #await message.author.dm_channel.send('I can\'t seem to find ModMail.')
                return

            channels = category.text_channels

            userChannel = 0

            embed = discord.Embed(
                title = message.author.name + ' says:',
                description = message.content,
                color = discord.Color.teal()
            )

            for channel in channels:
                if channel.name.endswith(str(message.author.id)):
                    userChannel = channel.id
                    #await message.author.dm_channel.send('I\'ve found the channel.')

            #if yes, send their msg in that category
            if userChannel != 0:
                #await message.author.dm_channel.send('I\'m sending into an existing channel.')
                chn = guild.get_channel(userChannel)
                await chn.send(embed = embed)
            #if not, create new channel then send msg
            else:
                #await message.author.dm_channel.send('I\'m creating a new channel.')
                newChannel = await guild.create_text_channel('MM-' + message.author.name + '-' + str(message.author.id), category = category)
                await newChannel.send('__New ModMail ticket created by **' + message.author.name + '**.__ <@&592070664169455616>')

                await newChannel.send(embed = embed)
        elif not(message.content.startswith('+')) and not(message.content.startswith('=')) and (message.channel.name.startswith('mm-') and ('Angels' in [role.name for role in message.author.roles] or 'mechanic' in [role.name for role in message.author.roles])):
            channel = message.channel
            userID = int(channel.name[channel.name.rfind('-')+1:])

            #user = self.client.get_user(userID)
            #user = discord.Client.get_user(userID, userID)
            user = discord.utils.get(self.client.get_all_members(), id=userID)

            embed = discord.Embed(
                title = 'A Mind Café Staff Member says:',
                description = message.content,
                color = discord.Color.teal()
            )
            #if (user == None):
            #    await message.author.dm_channel.send('No user found: ' + str(userID))
            #else:
            #    await self.send_message(user, "A message for you")
            #await client.send_message(some_user, "content")

            await user.send(embed = embed)
            #await message.author.dm_channel.send('userID: ' + str(userID))



def setup(client):
    client.add_cog(ModMail(client))
