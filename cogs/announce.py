import discord
from discord.ext import commands

class Announce(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def verify(self, ctx):
        if 'mechanic' in [role.name for role in ctx.message.author.roles]:
            embed = discord.Embed(
                color = discord.Color.teal(),
                title = '**Welcome to Mind Café!**',
                description = 'Be sure to read `#rules` for our server rules.'
            )

            embed.set_footer(text = 'Thanks for joining our family!')
            embed.set_thumbnail(url = 'https://cdn.discordapp.com/emojis/593214693573787654.png')

            embed.add_field(name = '**You are currently unverified.**',
            value = 'Please take a second to verify yourself by saying: `?verify`\n\nAsk a Mod if you need assistance!')

            await ctx.send(embed = embed)
        else:
            embed = discord.Embed(
                title = 'Sorry, you don\'t have permission to do that!',
                color = discord.Color.teal()
            )
            await ctx.send(embed = embed)

    @commands.command()
    async def mindcafe(self, ctx):
        if 'mechanic' in [role.name for role in ctx.message.author.roles]:
            embed = discord.Embed(
                color = discord.Color.teal(),
                title = '**Welcome to Mind Café**',
                description = 'We aim to prove others with a place of support and comfort. When you need a friend, someone to listen, or a place to socialize, we\'ll be here for you.'
            )

            embed.add_field(name = 'Have feedback, a question, or a repeal request?',
            value = 'Please contact one of our moderators (@mods) or use ModMail by simply messaging our bot Bean the Corgi.')

            embed.add_field(name = 'Want to apply to join our staff team?',
            value = 'Applications are always open and reviewed on a rolling basis. You do not need to resubmit unless you are scrapping your old submission. Link: https://forms.gle/bm9WS95hdWLr3TEG9')

            embed.add_field(name = 'How does this work?',
            value = 'Anyone can volunteer as a listener and devote their time to helping others, though they\'re also always welcome to ask for support themselves. Want to help others and become a listener? Get the role in #roles!')

            embed.set_thumbnail(url = 'https://cdn.discordapp.com/attachments/591611902459641856/595372970843701258/Mind_Cafe_Icon.png')

            await ctx.send(embed = embed)
        else:
            embed = discord.Embed(
                title = 'Sorry, you don\'t have permission to do that!',
                color = discord.Color.teal()
            )
            await ctx.send(embed = embed)

    @commands.command()
    async def rules(self, ctx):
        if 'mechanic' in [role.name for role in ctx.message.author.roles]:
            embed = discord.Embed(
                color = discord.Color.teal(),
                title = '**Mind Café Server Rules**',
                description = 'Need help? Message a moderator (@mods) or Bean for ModMail!'
            )

            embed.set_footer(text = 'By joining and participating in our server you agree to abide by our server rules and respect our staff decisions.')

            embed.add_field(name = '1) English only',
            value = 'Conversation and moderation flows more easily in a language all of us knows.')

            embed.add_field(name = '2) Names with QWERTY characters only',
            value = 'We should be able to use a QWERTY keyboard to type your name out and tag you.')

            embed.add_field(name = '3) We are a SFW server',
            value = 'Anything outside of the NSFW-labeled channels should be non-explicit. In the NSFW channels, nudity and pornography are not permitted.')

            embed.add_field(name = '4) Be respectful',
            value = 'We won\'t stand for any discrimination or \"jokes\" against others about their race, religion, sexuality, gender, political views, and more.')

            embed.add_field(name = '5) You do NOT talk about Fight Club',
            value = 'Anything posted in this server should not be shared outside of it, and we ask that our listeners follow the same rule with support DMs.')

            embed.add_field(name = '6) #no-reply and #nsfw-no-reply',
            value = 'Do not reply to any posts in these channels. No content can be directed towards or contain content from any current members in Mind Café; this includes pictures, even if they are censored.')

            embed.add_field(name = '7) #controversial',
            value = 'If you are found to be unable to handle the topics in controversial or you are taking the discussion to hate-speech or insults, you will have your controversial access removed from you.')

            embed.add_field(name = '8) If you are in a crisis, seek professional help',
            value = 'We are not a replacement for trained, professional resources. If you find yourself in danger of harming yourself or others, or being harmed by others, please contact your local emergency service.')

            await ctx.send(embed = embed)
        else:
            embed = discord.Embed(
                title = 'Sorry, you don\'t have permission to do that!',
                color = discord.Color.teal()
            )
            await ctx.send(embed = embed)

def setup(client):
    client.add_cog(Announce(client))
