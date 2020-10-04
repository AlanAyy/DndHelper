import json

import discord
from discord.ext import commands


class Dnd(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.combats = {}
        self.characters = {}

    @commands.command(aliases=['ch', 'char'])
    async def character(self, ctx, arg1, *args):
        author = ctx.message.author
        if arg1 == 'new':
            await self.Character.new(ctx, *args)
        elif arg1 == 'get':
            await self.Character.get(ctx, *args)
        elif arg1 == 'edit':
            await self.Character.edit(ctx, *args)
        elif arg1 in ['remove', 'del']:
            await self.Character.delete(ctx, *args)

    class Character:

        @classmethod
        async def new(cls, ctx, *args):
            # Lol car keys
            char_keys = ['race', 'class', 'lvl', 'str', 'dex', 'con', 'int', 'wis', 'cha']
            if args is None:
                e = discord.Embed(color=discord.Colour.gold())
                e.add_field(name='Command usage:', value='!character new [name] [%s]' % '] ['.join(char_keys))
                await ctx.send(embed=e)
                return
            char_dict = {}
            counter = -2
            for val in args:
                counter += 1
                # Assign a value to each key
                if counter == -1:
                    continue
                char_dict[char_keys[counter]] = val
            author = ctx.message.author
            name = args[0]
            formatted = {author: {name: {char_dict}}}
            with open('settings/characters.json', 'r+') as fp:
                json.dump(formatted, fp, indent=4)

        @classmethod
        async def get(cls, ctx, *args):
            await ctx.send(embed=discord.Embed(title='Under Construction!'))
            pass

        @classmethod
        async def edit(cls, ctx, *args):
            await ctx.send(embed=discord.Embed(title='Under Construction!'))
            pass

        @classmethod
        async def delete(cls, ctx, *args):
            await ctx.send(embed=discord.Embed(title='Under Construction!'))
            pass

    @commands.command(aliases=['c', 'battle', 'fight'])
    async def combat(self, ctx, arg1, *args):
        author = ctx.message.author
        combat = self.combats.get(author.id)
        if combat is not None:
            if arg1 == 'back':
                await combat.back()
            elif arg1 == 'next':
                await combat.next()
            elif arg1 == 'add':
                await combat.add(*args)
            elif arg1 in ['remove', 'del']:
                await combat(args[0])
            elif arg1 == 'end':
                await combat.end()
                del combat
            try:
                await ctx.message.delete()
            except discord.errors.Forbidden:
                print('Error! Missing `manage_messages` permission!')
        elif arg1 in ['start', 'new']:
            self.combats[author.id] = self.Combat()
            await self.combats[author.id].start(ctx, *args)

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        # Using dict.get here so it returns None and not an error
        r_combat = self.combats.get(user.id)
        if r_combat is not None:
            if user.id == r_combat.author and reaction.message == r_combat.msg:
                if reaction.emoji == self.combat.emoji['left']:
                    await self.combat.back()
                elif reaction.emoji == self.combat.emoji['right']:
                    await self.combat.next()
                try:
                    await reaction.remove(user)
                except discord.errors.Forbidden:
                    print('Error! Missing `manage_messages` permission!')

    class Combat:

        msg = None
        characters = []
        author = None  # Will hold the original message's author (the one who typed '!battle start')
        emoji = {'left': '\u25c0', 'right': '\u25b6'}
        turn = 0

        @classmethod
        async def start(cls, ctx, *args):
            for char in args:
                cls.characters.insert(len(cls.characters), char.split(',')[0])
            cls.author = ctx.message.author
            cls.msg = await ctx.send(embed=discord.Embed(title='Starting Combat...'))
            cls.bot = ctx.bot
            await cls._update()

        @classmethod
        async def _update(cls):
            string = ''
            e = discord.Embed(title='%s\'s Combat' % cls.author, colour=discord.Colour.red())
            for char in cls.characters:
                string += char + '\n'
            e.add_field(name='Initiative', value=string)
            await cls.msg.edit(embed=e)
            await cls.msg.add_reaction(cls.emoji.get('left'))
            await cls.msg.add_reaction(cls.emoji.get('right'))

        @classmethod
        async def back(cls):
            char = cls.characters[len(cls.characters) - 1]
            cls.characters.remove(char)
            cls.characters.insert(0, char)
            await cls._update()

        @classmethod
        async def next(cls):
            char = cls.characters[0]
            cls.characters.remove(char)
            cls.characters.insert(len(cls.characters), char)
            await cls._update()

        @classmethod
        async def add(cls, index, char):
            cls.characters.insert(int(index) - 1, char)
            await cls._update()

        @classmethod
        async def remove(cls, char):
            cls.characters.remove(char)
            await cls._update()

        @classmethod
        async def end(cls):
            await cls.msg.edit(embed=discord.Embed(title='Combat over!'))
            try:
                await cls.msg.clear_reactions()
            except discord.errors.Forbidden:
                print('Error! Missing `manage_messages` permission!')


def setup(bot):
    bot.add_cog(Dnd(bot))
