import os

import discord

from music import Music
from mytoken import getToken

intents = discord.Intents.all()
bot = discord.ext.commands.Bot(command_prefix="$", intents=intents)

MSG_ENABLED = False
ROLE = "aąbcćdeęfghijklłmnoóprsśtuwyzżźxqv1234567890?"
AUTO_ROLE = ["ktoś", "DJ"]
BANNED_USERS = {}


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
        if MSG_ENABLED:
            await createRoles(guild)
    print("Running!")


@bot.event
async def on_member_join(member):
    ban = BANNED_USERS.get(member.guild.id)
    if ban:
        for b in ban:
            if b == member:
                return
    for n in AUTO_ROLE:
        r = discord.utils.get(member.guild.roles, name=n)
        await member.add_roles(r)


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
    if not MSG_ENABLED:
        embed = discord.Embed(
            title="Error",
            description="This function is disabled",
            color=discord.Color.red(),
        )
        await ctx.send(embed=embed)
        return
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
    if not MSG_ENABLED:
        embed = discord.Embed(
            title="Error",
            description="This function is disabled",
            color=discord.Color.red(),
        )
        await ctx.send(embed=embed)
        return
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
    if not MSG_ENABLED:
        embed = discord.Embed(
            title="Error",
            description="This function is disabled",
            color=discord.Color.red(),
        )
        await ctx.send(embed=embed)
        return
    roles = await createRoles(ctx.guild)
    for r in roles:
        await ctx.author.remove_roles(r)
    embed = discord.Embed(
        title="Sub",
        description="Done!",
        color=discord.Color.green(),
    )
    await ctx.send(embed=embed)


@bot.command(pass_context=True, description="Remove user auto roles and ban them")
async def mute(ctx, *, name: str):
    if ctx.author.name != "jaanonim":
        embed = discord.Embed(
            title="Unmute",
            description=f"You cannot do this",
            color=discord.Color.red(),
        )
        await ctx.send(embed=embed)
        return
    server = ctx.author.guild
    user = discord.utils.get(server.members, name=name)
    if not user:
        embed = discord.Embed(
            title="Mute",
            description=f"User '{name}' not found!",
            color=discord.Color.red(),
        )
        await ctx.send(embed=embed)
        return
    if not BANNED_USERS.get(server.id):
        BANNED_USERS[server.id] = []
    BANNED_USERS[server.id].append(user)
    for n in AUTO_ROLE:
        r = discord.utils.get(server.roles, name=n)
        await user.remove_roles(r)

    embed = discord.Embed(
        title="Mute",
        description=f"Done! On user '{name}'",
        color=discord.Color.green(),
    )
    await ctx.send(embed=embed)


@bot.command(pass_context=True, description="Add user auto roles and unban them")
async def unmute(ctx, *, name: str):
    server = ctx.author.guild
    if ctx.author.name != "jaanonim":
        for u in BANNED_USERS:
            if u == name:
                BANNED_USERS[server.id].remove(u)
        embed = discord.Embed(
            title="Unmute",
            description=f"You cannot do this",
            color=discord.Color.red(),
        )
        await ctx.send(embed=embed)
        return
    user = discord.utils.get(server.members, name=name)
    if not user:
        embed = discord.Embed(
            title="Unute",
            description=f"User '{name}' not found!",
            color=discord.Color.red(),
        )
        await ctx.send(embed=embed)
        return
    if not BANNED_USERS.get(server.id):
        try:
            BANNED_USERS[server.id].remove(user)
        except:
            pass
    for n in AUTO_ROLE:
        r = discord.utils.get(server.roles, name=n)
        await user.add_roles(r)

    embed = discord.Embed(
        title="Unmute",
        description=f"Done! On user '{name}'",
        color=discord.Color.green(),
    )
    await ctx.send(embed=embed)


bot.add_cog(Music(bot))


bot.run(getToken())
