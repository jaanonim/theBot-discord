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


@bot.command(pass_context=True)
async def ha(ctx):
    guild = ctx.guild
    user = ctx.author
    role = discord.utils.get(guild.roles, name=user.name)
    if not role:
        role = await guild.create_role(name=user.name)
    await role.edit(color=discord.Colour.random())
    await user.add_roles(role)


@bot.command(pass_context=True)
async def aboute(ctx):
    await ctx.send("Author: jaanonim")


bot.add_cog(Music(bot))


token = os.getenv("TOKEN")
bot.run(token)
