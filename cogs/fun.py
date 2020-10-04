import random

import discord
from discord.ext import commands


class Fun(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['r', 'dice'])
    async def roll(self, ctx, dice):
        """Rolls dice. !roll [n]d[s], where [n] is the amount of dice and [s] is the sides."""
        dice_amount, dice_type = [int(i) for i in dice.split('d')]
        rolls = [random.randint(1, dice_type) for _ in range(dice_amount)]
        e = discord.Embed(title='%s\'s Rolls' % ctx.author, colour=0xffffff)
        e.add_field(name='Total', value=str(sum(rolls)))
        e.add_field(name='Rolls', value='%s' % ', '.join(map(str, rolls)))
        await ctx.send(embed=e)


def setup(bot):
    bot.add_cog(Fun(bot))
