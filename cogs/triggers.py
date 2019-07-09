import discord
from discord.ext import commands

class Triggers(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message):
        return

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        guild = self.client.get_guild(257751892241809408)
        casual = guild.get_channel(257751892241809408)
        
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
