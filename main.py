import os

import discord

from music import Music

intents = discord.Intents.all()
bot = discord.ext.commands.Bot(command_prefix="$", intents=intents)


@bot.event
async def on_ready():
    print("Running!")


@bot.event
async def on_member_join(member):
    await member.add_roles(discord.utils.get(member.guild.roles, name="🅾Gracze"))
    await member.add_roles(discord.utils.get(member.guild.roles, name="DJ"))


@bot.command(pass_context=True, aliases=["c", "ha"], description="Give random color")
async def color(ctx):
    guild = ctx.guild
    user = ctx.author
    role = discord.utils.get(guild.roles, name=user.name)
    if not role:
        role = await guild.create_role(name=user.name)
    c = discord.Colour.random()
    await role.edit(color=c)
    await user.add_roles(role)
    embed = discord.Embed(
        title="Colors",
        description=f"{ctx.author.mention} have new color! ✨",
        color=c,
    )
    await ctx.send(embed=embed)


@bot.command(pass_context=True, aliases=["author"], description="Aboute bot")
async def aboute(ctx):
    embed = discord.Embed(
        title="Aboute",
        description="Author: jaanonim",
        color=discord.Color.green(),
    )
    await ctx.send(embed=embed)


bot.add_cog(Music(bot))


token = os.getenv("TOKEN")
bot.run(token)
