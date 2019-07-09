import discord
import random
from discord.ext import commands

class Actions(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(pass_context=True)
    async def pat(self, ctx, user: discord.Member = None, *, msg = ''):
        responses = ['https://cdn.discordapp.com/attachments/257751892241809408/597979644725166097/unknown.gif',
        'https://i.gifer.com/7A80.gif',
        'https://media1.tenor.com/images/9bd2eb038544102aa4bb36fb8b0d01f9/tenor.gif?itemid=12437651',
        'https://25.media.tumblr.com/14be64e13a802d9b16063411134f29b7/tumblr_mfz90qdzaV1r4az5so1_400.gif',
        'https://media.tenor.com/images/dfe3267cca9596be840fbf9d5e86b747/tenor.gif',
        'https://media1.tenor.com/images/d6a91b652fd260f7d063bee23cd7f9ee/tenor.gif?itemid=8102480',
        'https://data.whicdn.com/images/38611077/original.gif',
        'https://media1.tenor.com/images/ca552807b4720928130e5f188cfbe2c9/tenor.gif?itemid=8061431',
        'https://media.giphy.com/media/Epd1qTKdonBhC/giphy-downsized-large.gif',
        'https://thumbs.gfycat.com/AlarmedAmpleFox-size_restricted.gif',
        'https://media1.tenor.com/images/b89e2aa380639d37b9521b72a266d498/tenor.gif?itemid=4215410']

        actionName = 'patted'

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
                title = 'pat pat'
            )
            embed.set_image(url = random.choice(responses))

            await ctx.send(embed = embed)


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
    async def hug(self, ctx, user: discord.Member = None, *, msg = ''):
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
