import discord
from discord.ext import commands

class Cmd(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['commands', 'cmds', 'command'])
    async def cmd(self, ctx):
        if 'mods' in [role.name for role in ctx.message.author.roles] or 'mechanic' in [role.name for role in ctx.message.author.roles]:
            embed = discord.Embed(
                title = 'Command List',
                description = '`<Required>, [Optional]`\n`[A]` = Admins, `[M]` = Mods+, `[E]` = Everyone\nPrefix: `+`',
                color = discord.Color.teal()
            )

            embed.set_footer(text = 'If you need any help, please contact a moderator.')
            #embed.set_image(url = 'https://cdn.discordapp.com/attachments/591611902459641856/592203509487894528/BEAN.png')
            embed.set_thumbnail(url = 'https://cdn.discordapp.com/emojis/592846424899715079.png')
            #embed.set_author(name = 'Author Name', icon_url = 'https://i.etsystatic.com/9905287/r/il/030f27/1483225420/il_570xN.1483225420_kjim.jpg')

            embed.add_field(name = 'Meta',
            value = '`[M] cmd` - This! (commands, command, cmds)\n`[E] info` - Bot information.\n`[E] ping` - Pings the bot instance.\n', inline = True)
            embed.add_field(name = 'Mod',
            value = '`[A] status <message>` - Changes the bot\'s activity status.', inline = True)

            embed.add_field(name = 'Echo',
            value = '`[A] echo <#channel> <message>` - Uses the bot to send the message to the specified channel.', inline = False)
            embed.add_field(name = 'ModMail',
            value = 'Value', inline = False)
            embed.add_field(name = 'Support',
            value = 'Value', inline = False)

            await ctx.send(embed = embed)
        else:
            embed = discord.Embed(
                title = 'Sorry, you don\'t have permission to do that!',
                color = discord.Color.teal()
            )
            await ctx.send(embed = embed)

def setup(client):
    client.add_cog(Cmd(client))
