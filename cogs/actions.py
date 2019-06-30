import discord
import random
from discord.ext import commands

class Actions(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def blep(self, ctx):
        responses = ['https://media1.tenor.com/images/abf08100392109094617cb59eb159486/tenor.gif?itemid=3437296',
        'https://media2.giphy.com/media/SewaEY6yMH6x2/giphy.gif',
        'https://media1.giphy.com/media/muPGAcnm1YCoZA50jQ/giphy.gif',
        'https://66.media.tumblr.com/493e8df5839f92e8b5632050797c23a8/tumblr_pml5x2Dm7f1w9j4ono1_540.gif',
        'https://thumbs.gfycat.com/DentalDarlingCardinal-size_restricted.gif',
        'https://thumbs.gfycat.com/AntiqueGrayHyrax-size_restricted.gif',
        'http://cdn.funnyisms.com/24ce5866-24d1-4fc7-8ac4-92111f4e5d95.gif',
        'http://the.earth.li/~jon/junk/blep.gif',
        'https://s.mltshp.com/r/1F8ND',
        'https://media.giphy.com/media/Y9MJ0otgR03yE/giphy.gif']
        embed = discord.Embed(
            title = 'mlem',
            color = discord.Color.teal()
        )
        embed.set_image(url = random.choice(responses))

        await ctx.send(embed = embed)

    @commands.command(pass_context=True)
    async def hug(self, ctx, user: discord.Member = None, *, msg):
        responses = ['https://media1.giphy.com/media/Lb3vIJjaSIQWA/source.gif',
        'https://treasuredscriptcom.files.wordpress.com/2018/09/hiro-hugging-baymax1.gif',
        'https://media.giphy.com/media/17Q92poP1qJwI/giphy.gif',
        'https://gifrific.com/wp-content/uploads/2015/05/Sloth-Hugs-Toy-Animal-and-Falls-Over.gif',
        'https://media.giphy.com/media/6dsQ68HCZZ1xm/giphy.gif',
        'https://66.media.tumblr.com/487912f009d7545d1cee698d68d12e5d/tumblr_pdx639rmL51rhmoixo1_400.gif',
        'https://media2.giphy.com/media/ZaBHSbiLQTmFi/source.gif',
        'https://media3.giphy.com/media/hdOrhnBB6Enuw/source.gif',
        'https://i.pinimg.com/originals/f3/48/a9/f348a9ffee1943fbe248fa2dc7eb3f19.gif',
        'https://66.media.tumblr.com/51a12abd75d1f8f6f9a3846e6d2bd528/tumblr_inline_nmm9z1X2sS1s8zbfz_500.gif',
        'https://66.media.tumblr.com/c27d1adbe7410191d24c8f62a68695a9/tumblr_inline_nmmazxORzb1s8zbfz_500.gif']
        #embed = action(user, random.choice(responses), 'hugged')

        actionName = 'hugged'

        if (user != None):
            embed = discord.Embed(
                color = discord.Color.teal(),
                title = '**' + user.name + '**, you\'ve just been ' + actionName + '!'
            )
            embed.set_image(url = random.choice(responses))

            await ctx.send(embed = embed)

        else:
            embed = discord.Embed(
                color = discord.Color.teal(),
                title = 'hugs!'
            )
            embed.set_image(url = random.choice(responses))

            await ctx.send(embed = embed)


        #embed.set_image(url = random.choice(responses))

        #await ctx.send(embed = embed)

def setup(client):
    client.add_cog(Actions(client))

'''
async def action(user: discord.Member, gif, actionName):
    embed = discord.Embed(
        title = discord.Member.mention + ', you\'ve just been ' + action + '!',
        color = discord.Color.teal()
    )
    embed.set_image(url = gif)

    return embed
    #await ctx.send(embed = embed)
'''
