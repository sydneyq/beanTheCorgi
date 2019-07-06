import discord
from discord.ext import commands

class Announce(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def mcRolesHelp(self, ctx):
        if 'mechanic' in [role.name for role in ctx.message.author.roles]:
            embed = discord.Embed(
                color = discord.Color.teal(),
                description = 'React with the corresponding emoji to obtain/remove a role.'
            )

            embed.add_field(name = 'Helping Others Roles',
            value = '🤝 - <@&300743585584906240>\nWant to be on the forefront of helping others? Become a listener and you\'ll get pinged whenever someone needs support!\n\n🎲 - <@&591484837932695582>\nGet notified whenever someone is bored and would like to socialize.\n\n🚀 - <@&591484887018766336>\n Get notified whenever someone is lonely and in need of a friend.')

            await ctx.send(embed = embed)
        else:
            embed = discord.Embed(
                title = 'Sorry, you don\'t have permission to do that!',
                color = discord.Color.teal()
            )
            await ctx.send(embed = embed)

    @commands.command()
    async def mcRolesAccess(self, ctx):
        if 'mechanic' in [role.name for role in ctx.message.author.roles]:
            embed = discord.Embed(
                color = discord.Color.teal(),
                description = 'React with the corresponding emoji to obtain/remove a role.'
            )

            embed.add_field(name = 'Access Roles',
            value = '⚠ - <@&445667601386045450>\nGet access to our NSFW channels! Please read <#595375736966348810> before getting this role.\n\nWant access to <@&579371787394220110>? Ask one of our moderators!')

            await ctx.send(embed = embed)
        else:
            embed = discord.Embed(
                title = 'Sorry, you don\'t have permission to do that!',
                color = discord.Color.teal()
            )
            await ctx.send(embed = embed)

    @commands.command()
    async def mcRolesIdentity(self, ctx):
        if 'mechanic' in [role.name for role in ctx.message.author.roles]:
            embed = discord.Embed(
                color = discord.Color.teal(),
                description = 'React with the corresponding emoji to obtain/remove a role.'
            )

            embed.add_field(name = 'Identity Roles',
            value = '🚺 - <@&446123400008564739>\n\n🚹 - <@&446123379997540402>\n\n🕵 - <@&446123416903483392>')

            await ctx.send(embed = embed)
        else:
            embed = discord.Embed(
                title = 'Sorry, you don\'t have permission to do that!',
                color = discord.Color.teal()
            )
            await ctx.send(embed = embed)

    @commands.command()
    async def mcRolesPing(self, ctx):
        if 'mechanic' in [role.name for role in ctx.message.author.roles]:
            embed = discord.Embed(
                color = discord.Color.teal(),
                description = 'React with the corresponding emoji to obtain/remove a role.'
            )

            embed.add_field(name = 'Ping Roles',
            value = '👑 - <@&596053595548549150>\nFor our real up-to-date enthusiasts! Get pinged about every little announcement, partnership, or public change.\n\n🎉 - <@&595088852323139604>\nGet notified for any online events hosted for the community!\n\n📣 - <@&596053605065162948>\nGet notified for everything important happening in Mind Café!')

            await ctx.send(embed = embed)
        else:
            embed = discord.Embed(
                title = 'Sorry, you don\'t have permission to do that!',
                color = discord.Color.teal()
            )
            await ctx.send(embed = embed)

    @commands.command()
    async def mcRolesTop(self, ctx):
        if 'mechanic' in [role.name for role in ctx.message.author.roles]:
            embed = discord.Embed(
                color = discord.Color.teal(),
                title = '**Welcome to the Roles Channel!**',
                description = 'Here, you\'ll find everything you\'ll need to know about all of our roles.'
            )

            embed.set_thumbnail(url = 'https://cdn.discordapp.com/emojis/594982856162541573.png')

            embed.add_field(name = '**Staff Roles**',
            value = '<@&594652646611222538> - Administrative staff\n<@&592070664169455616> - Moderation staff\n<@&594642605862682672> - Event hosting and coordination staff\n<@&594642783160107186> - Partnership and marketing staff\n<@&591398563578380289> - Staff in-trial\n<@&257755582662967305> - All staff\n<@&445391150828748801> - Bots\n[Want to apply to join the staff team?](https://forms.gle/bm9WS95hdWLr3TEG9)')

            embed.add_field(name = '**Exclusive Roles**',
            value = '<@&591479293801136149> - 1 invites\n<@&591479443281674251> - 5 invites\n<@&591480362891345937> - 10 invites\n<@&588686697227616257> - Server nitro boosters\nCheck how many invites you have by using `%invites` in <#431191485933813765>.')

            await ctx.send(embed = embed)
        else:
            embed = discord.Embed(
                title = 'Sorry, you don\'t have permission to do that!',
                color = discord.Color.teal()
            )
            await ctx.send(embed = embed)


    @commands.command()
    async def mcVerify(self, ctx):
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
    async def mcAbout(self, ctx):
        if 'mechanic' in [role.name for role in ctx.message.author.roles]:
            embed = discord.Embed(
                color = discord.Color.teal(),
                title = '**Welcome to Mind Café!**',
                description = 'We aim to provide others with a place of support and comfort. When you need a friend, someone to listen, or a place to socialize, we\'ll be here for you.'
            )

            embed.add_field(name = 'Have feedback, a question, or a repeal request?',
            value = 'Please contact one of our moderators or use ModMail by simply messaging our bot Bean the Corgi.')

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
    async def mcRules(self, ctx):
        if 'mechanic' in [role.name for role in ctx.message.author.roles]:
            embed = discord.Embed(
                color = discord.Color.teal(),
                title = '**Mind Café Server Rules!**',
                description = 'Need help? Message a moderator (<@&592070664169455616>) or Bean for ModMail!'
            )

            embed.set_footer(text = 'By joining and participating in our server you agree to abide by our server rules and respect our staff decisions.')

            embed.add_field(name = '1) English only',
            value = 'Conversation and moderation flows more easily in a language all of us knows.')

            embed.add_field(name = '2) Names with QWERTY characters only',
            value = 'We should be able to use a QWERTY keyboard to type your name out and tag you.')

            embed.add_field(name = '3) We are a SFW server',
            value = 'Anything outside of the NSFW-labeled channels should be non-explicit. In the NSFW channels, nudity and pornography are not permitted.')

            embed.add_field(name = '4) Be respectful',
            value = 'Drama and insults is to be kept outside of the server. We also won\'t stand for any discrimination or \"jokes\" against others about their race, religion, sexuality, gender, political views, and more.')

            embed.add_field(name = '5) You do NOT talk about Fight Club',
            value = 'Anything posted in this server should not be shared outside of it, and we ask that our listeners follow the same rule with support DMs.')

            embed.add_field(name = '6) No advertising',
            value = 'This includes posting or promoting other server invites, publicly or in DMs, and personal social media if done too often.')

            embed.add_field(name = '7) No unnecessary or unallowed pinging',
            value = 'Do not ping roles without reason, and spam pinging roles or members is strictly prohibited. All roles except for Help roles and Staff roles should not be pinged by non-staff.')

            embed.add_field(name = '8) No-Reply channels',
            value = 'Do not reply to any posts in these channels. No content can be directed towards or contain content from any current members in Mind Café; this includes pictures, even if they are censored.')

            embed.add_field(name = '9) Controversial channels',
            value = 'If you are found to be unable to handle the topics in controversial or you are taking the discussion to hate-speech or insults, you will have your controversial access removed from you.')

            embed.add_field(name = '10) Check-in channels',
            value = 'Please do not have any conversations in these channels, for that is not the purpose of them.')

            embed.add_field(name = '11) Support channels',
            value = 'When asking for public support, the topic cannot be about or relating to anyone else in the server who can possibly see your conversation. Those support requests should be through DM only. Any venting, upsetting, or support topics should be in support channels (channels in the Support categories) only.')

            embed.add_field(name = '12) If you are in a crisis, seek professional help',
            value = 'We are not a replacement for trained, professional resources. If you find yourself in danger of harming yourself or others, or being harmed by others, please contact your [local emergency services](https://en.wikipedia.org/wiki/List_of_emergency_telephone_numbers).')

            embed.add_field(name = '13) Discord Above All, Hail Discord',
            value = 'In addition to the rules above, we enforce [Discord\'s ToS](https://discordapp.com/terms) and [Guidelines](https://discordapp.com/guidelines).')

            await ctx.send(embed = embed)
        else:
            embed = discord.Embed(
                title = 'Sorry, you don\'t have permission to do that!',
                color = discord.Color.teal()
            )
            await ctx.send(embed = embed)

def setup(client):
    client.add_cog(Announce(client))
