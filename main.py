import os

import discord

from music import Music

intents = discord.Intents.all()
bot = discord.ext.commands.Bot(command_prefix="$", intents=intents)

ROLE = "aąbcćdeęfghijklłmnoóprsśtuwyzżźxqv1234567890?"


async def createRoles(guild):
    roles = []
    for name in ROLE:
        role = discord.utils.get(guild.roles, name=name)
        if not role:
            c = discord.Colour.random()
            role = await guild.create_role(name=name, color=c)
        roles.append(role)
    return roles


@bot.event
async def on_ready():
    for guild in bot.guilds:
        await createRoles(guild)
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


@bot.command(pass_context=True, aliases=["eee"], description="Send encoded message")
async def msg(ctx, *, message: str):
    guild = ctx.guild
    message = message.lower()
    result = ""

    for char in message:
        if char == " ":
            result += "   "
            continue
        role = discord.utils.get(guild.roles, name=char)
        if role:
            result += role.mention
        else:
            result += char

    await ctx.send(result)


@bot.command(pass_context=True, description="Add user all 'abc' roles")
async def add(ctx):
    roles = await createRoles(ctx.guild)
    for r in roles:
        await ctx.author.add_roles(r)
    embed = discord.Embed(
        title="Add",
        description="Done!",
        color=discord.Color.green(),
    )
    await ctx.send(embed=embed)


@bot.command(pass_context=True, description=" Remove user all 'abc' roles")
async def sub(ctx):
    roles = await createRoles(ctx.guild)
    for r in roles:
        await ctx.author.remove_roles(r)
    embed = discord.Embed(
        title="Sub",
        description="Done!",
        color=discord.Color.green(),
    )
    await ctx.send(embed=embed)


bot.add_cog(Music(bot))


token = os.getenv("TOKEN")
bot.run(token)
