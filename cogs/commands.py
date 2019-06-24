import discord
from discord.ext import commands

class Commands(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['cmd', 'cmds', 'command'])
    async def commands(self, ctx):
        embed = discord.Embed(
            title = 'Commands',
            description = '(Commands)',
            color = discord.Color.blue()
        )

        embed.set_footer(text = 'footer')
        embed.set_image(url = 'https://cdn.discordapp.com/attachments/591611902459641856/592203509487894528/BEAN.png')
        embed.set_thumbnail(url = 'https://s-media-cache-ak0.pinimg.com/736x/9b/62/6f/9b626faf411f30523487e16f068b354d.jpg')
        embed.set_author(name = 'Author Name', icon_url = 'https://i.etsystatic.com/9905287/r/il/030f27/1483225420/il_570xN.1483225420_kjim.jpg')
        embed.add_field(name = 'Field Name', value = 'Field Value', inline = False)
        
        await ctx.send(embed = embed)

def setup(client):
    client.add_cog(Commands(client))
