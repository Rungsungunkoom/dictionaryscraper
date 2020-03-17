import os
import discord
import asyncio
import pdb
import schedule
import wordquery
import json
from discord_argparse import ArgumentConverter, OptionalArgument, RequiredArgument
from discord.ext import commands

guild = os.getenv('DISCORD_GUILD')
token = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')

rword_param_converter = ArgumentConverter(
    number = OptionalArgument(
        int, 
        doc="The number of words to get.",
        default=1
    ),
    startswith = OptionalArgument(
        str,
        doc="Words that start with this value.",
        default=""
    ),
    endswith = OptionalArgument(
        str,
        doc="Words that end with this value.",
        default=""
    )
)

@bot.command()
async def rword(ctx, *, params:rword_param_converter=rword_param_converter.defaults()):
    try:
        responses = wordquery.getRandomWord("dictionary.db", params['number'], params['startswith'], params['endswith'])

        if len(responses) == 0:
            await ctx.send("Sorry, I got nothing :(")
            return

        if len(responses) < params['number']:
            if len(responses) == 1:
                await ctx.send("I only have " + str(len(responses)) + " result, but here it is...")
            else:
                await ctx.send("I only have " + str(len(responses)) + " results, but here they are...")

        for resp in responses:
            payload = json.loads(resp[0])
            embed = discord.Embed(title=payload.get('title'), url=payload.get('url'), description=payload.get('description'))
            await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send(str(e))

bot.run(token)