
    '''
    @commands.command()
    async def avatar(self, ctx, channel: discord.TextChannel = None):
        message = ctx.message
        if not self.meta.isAdmin(message.author):
            return

        if channel is None:
            channel = ctx.channel

        await ctx.message.delete()

        embed = discord.Embed(
            title = 'Game On: Avatar!',
            description = 'Bean is the Avatar and needs teachers from each element!',
            color = discord.Color.teal()
        )

        choices = ['Water', 'Air', 'Fire', 'Earth']
        result = random.choice(choices)
        pic = ''

        if result == 'Water':
            pic = 'http://dpegb9ebondhq.cloudfront.net/product_photos/15204550/water-01_large.jpg'
        elif result == 'Air':
            pic = 'https://d3u67r7pp2lrq5.cloudfront.net/product_photos/15204511/air-01_original.jpg'
        elif result == 'Fire':
            pic = 'https://dzasv7x7a867v.cloudfront.net/product_photos/15204544/Fire-01_original.jpg'
        elif result == 'Earth':
            pic = 'http://d3u67r7pp2lrq5.cloudfront.net/product_photos/15204526/earth-01_400w.jpg'

        embed.add_field(name='Affinity: ' + result, value='Get someone from your Squad with the correct Affinity to post the 💥 emoji before the other Squad to gain a point!')
        embed.set_thumbnail(url = pic)
        await channel.send(embed = embed)

        def check(m):
            return m.content.lower() == '💥' and m.channel == channel

        cont = True

        while (cont):
            msg = await self.client.wait_for('message', check=check)

            user = self.meta.getProfile(msg.author)

            if user['squad'] == '':
                embed = discord.Embed(
                    title = 'Sorry, you\'re not in a Squad yet! Join one by using `+squad tea/coffee`.',
                    color = discord.Color.teal()
                )
                await channel.send(embed = embed)
                cont = True
                continue
            elif user['affinity'] is None or user['affinity'] == '':
                embed = discord.Embed(
                    title = 'Sorry, you haven\'t set an affinity yet! You can do that by using `+affinity fire/water/air/earth`.',
                    color = discord.Color.teal()
                )
                await channel.send(embed = embed)
                cont = True
                continue
            elif user['affinity'] != result:
                embed = discord.Embed(
                    title = 'You don\'t have the required affinity! You\'re looking for someone who\'s `' + result + '`.',
                    color = discord.Color.teal()
                )
                await channel.send(embed = embed)
                cont = True
                continue
            elif user['affinity'] == result:
                cont = False

                squad = user['squad']
                if squad == 'Tea':
                    self.tea_score += 1
                else:
                    self.coffee_score += 1

                embed2 = discord.Embed(
                    title = msg.author.name + ' just earned `1` point for ' + squad + '!',
                    description = '**Tea Squad:** `' + str(self.tea_score) + '`\n**Coffee Squad:** `' + str(self.coffee_score) + '`',
                    color = discord.Color.teal()
                )

                if self.tea_score > self.coffee_score:
                    embed2.set_thumbnail(url = 'https://cdn.discordapp.com/attachments/591611902459641856/613918428293627914/teamteaBean.png')
                elif self.coffee_score > self.tea_score:
                    embed2.set_thumbnail(url = 'https://cdn.discordapp.com/attachments/591611902459641856/613918442034298890/teamcoffeeBean.png')


                await channel.send(embed = embed2)

                return
    '''
    '''
    @commands.command(aliases=['traffic', 'trafficlight', 'rlgl'])
    async def redlightgreenlight(self, ctx, channel: discord.TextChannel = None):
        message = ctx.message
        if not self.meta.isAdmin(message.author):
            return

        if channel is None:
            channel = ctx.channel

        await ctx.message.delete()

        which = ['pic', 'text']
        ref = random.choice(which)
        desc = 'Look at the text, not the picture!'

        if ref == 'pic':
            desc = 'Look at the picture, not the text!'

        embed = discord.Embed(
            title = 'Game On: Red Light, Green Light!',
            description = desc,
            color = discord.Color.teal()
        )

        elements = ['Red', 'Green', 'Yellow']
        weights = [0.45, 0.45, 0.10]
        text = choice(elements, p=weights)

        color_pics = ['https://upload.wikimedia.org/wikipedia/commons/thumb/1/13/Disc_Plain_red.svg/2000px-Disc_Plain_red.svg.png',
        'https://upload.wikimedia.org/wikipedia/commons/thumb/f/ff/Green_icon.svg/1024px-Green_icon.svg.png',
        'https://upload.wikimedia.org/wikipedia/en/thumb/f/fb/Yellow_icon.svg/1024px-Yellow_icon.svg.png']
        pic = choice(elements, p=weights)

        embed.add_field(name='Light: ' + text, value='Say `go` if the Light is Green, `stop` if the Light is Red, or `slow` if the Light is Yellow before the other Squad!\nWrong answers deduct points from your Squad. Getting a Yellow Light correct deducts from the other Squad!')

        url = color_pics[0]
        if pic == 'Green':
            url = color_pics[1]
        elif pic == 'Yellow':
            url = color_pics[2]

        embed.set_thumbnail(url = url)
        await channel.send(embed = embed)
        input = ''

        def check(m):
            nonlocal input
            input = m.content.lower()
            return (m.content.lower() == 'stop' or m.content.lower() == 'go' or m.content.lower() == 'slow') and m.channel == channel

        cont = True

        while (cont):
            msg = await self.client.wait_for('message', check=check)

            user = self.meta.getProfile(msg.author)

            if user['squad'] == '':
                embed = discord.Embed(
                    title = 'Sorry, you\'re not in a Squad yet! Join one by using `+squad tea/coffee`.',
                    color = discord.Color.teal()
                )
                await channel.send(embed = embed)
                cont = True
                continue
            else:
                cont = False
                correct = False
                answer = text

                if ref == 'pic':
                    answer = pic

                if answer == 'Red':
                    if input == 'stop':
                        correct = True
                elif answer == 'Green':
                    if input == 'go':
                        correct = True
                elif answer == 'Yellow':
                    if input == 'slow':
                        correct = True

                squad = user['squad']

                if correct:
                    if answer == 'Yellow':
                        opposquad = 'Tea'
                        if squad == 'Tea':
                            opposquad = 'Coffee'
                            self.coffee_score -= 10
                        else:
                            self.tea_score -= 10
                        embed2 = discord.Embed(
                            title = msg.author.name + ' just deducted `10` points from ' + opposquad + '!',
                            description = '**Tea Squad:** `' + str(self.tea_score) + '`\n**Coffee Squad:** `' + str(self.coffee_score) + '`',
                            color = discord.Color.teal()
                        )
                    else:
                        if squad == 'Tea':
                            self.tea_score += 5
                        else:
                            self.coffee_score += 5
                        embed2 = discord.Embed(
                            title = msg.author.name + ' just earned `5` points for ' + squad + '!',
                            description = '**Tea Squad:** `' + str(self.tea_score) + '`\n**Coffee Squad:** `' + str(self.coffee_score) + '`',
                            color = discord.Color.teal()
                        )
                else:
                    if squad == 'Tea':
                        self.tea_score -= 10
                    else:
                        self.coffee_score -= 10
                    embed2 = discord.Embed(
                        title = msg.author.name + ' just dropped ' + squad + '\'s score by `10` points!',
                        description = '**Tea Squad:** `' + str(self.tea_score) + '`\n**Coffee Squad:** `' + str(self.coffee_score) + '`',
                        color = discord.Color.teal()
                    )

                if self.tea_score > self.coffee_score:
                    embed2.set_thumbnail(url = 'https://cdn.discordapp.com/attachments/591611902459641856/613918428293627914/teamteaBean.png')
                elif self.coffee_score > self.tea_score:
                    embed2.set_thumbnail(url = 'https://cdn.discordapp.com/attachments/591611902459641856/613918442034298890/teamcoffeeBean.png')

                await channel.send(embed = embed2)

                return
    '''
    '''
    @commands.command(aliases=['pewpew', 'pewpewpew', 'teamwork', 'teambattle'])
    async def pew(self, ctx, channel: discord.TextChannel = None):
        message = ctx.message
        if not self.meta.isAdmin(message.author):
            return

        if channel is None:
            channel = ctx.channel

        await ctx.message.delete()

        embed = discord.Embed(
            title = 'Game On: Pewpew!',
            description = 'Get three people from your Squad to say \"pewpew\" first to gain a point!',
            color = discord.Color.teal()
        )

        await channel.send(embed = embed)

        isFull = False
        local_tea_score = 0
        local_coffee_score = 0

        tea_shooters = []
        coffee_shooters = []

        while not isFull:
            def check(m):
                return (m.content.lower() == 'pew pew' or m.content.lower() == 'pewpew') and m.channel == channel

            msg = await self.client.wait_for('message', check=check)

            user = self.dbConnection.findProfile({'id' : msg.author.id})
            if user is None:
                embed = discord.Embed(
                    title = 'Sorry, you don\'t have a profile yet! You can make one by using +profile.',
                    color = discord.Color.teal()
                )
                await channel.send(embed = embed)
                continue

            elif user['squad'] == '':
                embed = discord.Embed(
                    title = 'Sorry, you\'re not in a Squad yet! Join one by using `+squad tea/coffee`.',
                    color = discord.Color.teal()
                )
                await channel.send(embed = embed)
                continue

            squad = user['squad']

            if squad == 'Tea':
                if msg.author.id in tea_shooters:
                    embed = discord.Embed(
                        title = 'Sorry, you\'ve already shot in this round!',
                        color = discord.Color.teal()
                    )
                    await channel.send(embed = embed)
                    continue
                else:
                    tea_shooters.append(msg.author.id)

                local_tea_score += 1
            else:
                if msg.author.id in coffee_shooters:
                    embed = discord.Embed(
                        title = 'Sorry, you\'ve already shot in this round!',
                        color = discord.Color.teal()
                    )
                    await channel.send(embed = embed)
                    continue
                else:
                    coffee_shooters.append(msg.author.id)

                local_coffee_score += 1

            if local_tea_score == 3 or local_coffee_score == 3:
                isFull = True

            embed3 = discord.Embed(
                title = 'Current Attacks',
                color = discord.Color.teal()
            )

            tea_shooters_str = ''
            for shooter in tea_shooters:
                tea_shooters_str += '<@' + str(shooter) + '>\n'

            if tea_shooters_str == '':
                tea_shooters_str = 'N/A'

            embed3.add_field(name='Tea Shooters (' + str(len(tea_shooters)) + '/3)', value=tea_shooters_str)

            coffee_shooters_str = ''
            for shooter in coffee_shooters:
                coffee_shooters_str += '<@' + str(shooter) + '>\n'

            if coffee_shooters_str == '':
                coffee_shooters_str = 'N/A'

            embed3.add_field(name='Coffee Shooters (' + str(len(coffee_shooters)) + '/3)', value=coffee_shooters_str)

            await channel.send(embed = embed3)

        if local_tea_score == 3:
            self.tea_score += 1
        else:
            self.coffee_score += 1

        embed2 = discord.Embed(
            title = squad + ' Squad just earned `1` point!',
            description = '**Tea Squad:** `' + str(self.tea_score) + '`\n**Coffee Squad:** `' + str(self.coffee_score) + '`',
            color = discord.Color.teal()
        )

        await channel.send(embed = embed2)

        return
    '''

    #karaoke event
    '''
    @commands.Cog.listener()
    async def on_message(self, message):
        if not isinstance(message.channel, discord.TextChannel):
            return

        if ('karaoke' in message.channel.name):
            id = message.author.id
            if ('add me' in message.content.lower()):
                if id not in self.queue:
                    self.queue.append(id)
                    embed = discord.Embed(
                        title = 'Added you to the queue!',
                        color = discord.Color.teal()
                    )
                    await message.channel.send(embed = embed)
                else:
                    embed = discord.Embed(
                        title = 'You\'re already in the queue!',
                        color = discord.Color.teal()
                    )
                    await message.channel.send(embed = embed)
            elif ('remove me' in message.content.lower()):
                if id in self.queue:
                    embed = discord.Embed(
                        title = 'I\'ve removed you from the queue.',
                        color = discord.Color.teal()
                    )
                    await message.channel.send(embed = embed)

                    self.queue.remove(id)
                else:
                    embed = discord.Embed(
                        title = 'You\'re not in the queue!',
                        color = discord.Color.teal()
                    )
                    await message.channel.send(embed = embed)
            elif ('queue' in message.content.lower()):
                say = ''

                for id in self.queue:
                    say += self.client.get_user(id).name + '\n'
                embed = discord.Embed(
                    title = 'Current Queue',
                    color = discord.Color.teal(),
                    description = say
                )
                await message.channel.send(embed = embed)
            elif 'skip' == message.content.lower() and ('angels' in [role.name for role in message.author.roles] or 'mechanic' in [role.name for role in message.author.roles]):
                self.queue.pop()
                embed = discord.Embed(
                    title = 'I\'ve skipped to the next person.',
                    color = discord.Color.teal()
                )
                await message.channel.send(embed = embed)
                self.queue.remove(id)
    '''

    #team names in names event
    '''
    @commands.command(aliases=['snames'])
    async def squadnames(self, ctx):
        guild = ctx.guild
        members = guild.members

        embed = discord.Embed(
            title = 'Squad Names',
            color = discord.Color.teal()
        )

        tea = 0
        teaMembers = ''
        coffee = 0
        coffeeMembers = ''

        for member in members:
            if not self.meta.isVerified(member):
                continue
            if member.nick is not None:
                if self.meta.hasWord(member.nick, 'tea'):
                    tea += 1
                    teaMembers += '<@' + str(member.id) + '>\n'
                if self.meta.hasWord(member.nick, 'coffee'):
                    coffee += 1
                    coffeeMembers += '<@' + str(member.id) + '>\n'
            else:
                if self.meta.hasWord(member.name, 'tea'):
                    tea += 1
                    teaMembers += '<@' + str(member.id) + '>\n'
                if self.meta.hasWord(member.name, 'coffee'):
                    coffee += 1
                    coffeeMembers += '<@' + str(member.id) + '>\n'

        embed.add_field(name='Members with \"tea\"', value= '`' + str(tea) + '` Members\n' + teaMembers)
        embed.add_field(name='Members with \"coffee\"', value= '`' + str(coffee) + '` Members\n' + coffeeMembers)

        await ctx.send(embed = embed)
        return
    '''
