from discord.ext import commands
import discord
import os
from collections import Counter

bot = commands.Bot(command_prefix = '!')
# https://discordpy.readthedocs.io/en/stable/api.html#discord.PartialMessage to a set of tags
msg_tags = dict()
tag_msgs = dict() # TODO update rest of code # TODO refactor simultaneous maintenance
tag_usage = Counter()

MPMC_COMMAND_ERROR_MESSAGE = "bad message format. see https://discordpy.readthedocs.io/en/stable/ext/commands/api.html#discord.ext.commands.PartialMessageConverter"
class MyPartialMessageConverter(commands.PartialMessageConverter): # maybe convert to
  async def convert(cls, ctx, msg: str):
    ids = msg.rsplit('/', maxsplit=2)[-2:]
    if len(ids) == 1:
      ids = msg.split('-')
      if len(ids) == 2: # case: {channel ID}-{message ID}
        channel_id, msg_id = ids
        return bot.get_channel(int(channel_id)).get_partial_message(int(msg_id))
      elif len(ids) == 1: # case: message ID
        channel_id = ctx.channel.id
        msg_id = msg
        return bot.get_channel(int(channel_id)).get_partial_message(int(msg_id))
      else: raise commands.CommandError(MPMC_COMMAND_ERROR_MESSAGE)
    elif len(ids) == 2: # case: from URL
      channel_id, msg_id = ids
      return bot.get_channel(int(channel_id)).get_partial_message(int(msg_id)) # seems repetitive
    else: raise commands.CommandError(MPMC_COMMAND_ERROR_MESSAGE)

@bot.command() # i'd like to use slash commands or maybe even message commands, but idkh
async def tag(ctx, msg: MyPartialMessageConverter, *tags: str): # idk if PartialMessages are the best idea
  for tag in tags:
    tag_usage[tag] += 1
    if msg in msg_tags:
      msg_tags[msg].add(tag)
    else:
      msg_tags[msg] = {tag} # set(tag) would destructure into chars
    if tag in tag_msgs:
      tag_msgs[tag].add(msg)
    else:
      tag_msgs[tag] = {msg}
  print("RESULT !tag :")
  print(msg_tags)
  print(tag_msgs)
  print(tag_usage)

@bot.command()
async def untag(ctx, msg: MyPartialMessageConverter, *tags: str):
  global msg_tags # untested, I didn't have this before
  global tag_usage
  for tag in tags:
    try:
      msg_tags[msg].remove(tag)
      tag_msgs[tag].remove(msg)
      tag_usage[tag] -= 1
    except KeyError:
      pass
  print("RESULT !untag :")
  print(msg_tags)
  print(tag_usage)

@bot.command()
async def clean(ctx):
  global msg_tags
  global tag_msgs
  global tag_usage
  msg_tags = {k:v for k,v in msg_tags.items() if v}
  tag_msgs = {k:v for k,v in tag_msgs.items() if v}
  tag_usage = +tag_usage # removes entries \le 0
  print(msg_tags)
  print(tag_usage)

def pretty_print_list(list):
  result_msg = ""
  for item in list:
    result_msg += item + "\n"
  return result_msg

def pretty_print_dict(d: dict(), k_name: str, v_name: str):
  result_msg = ""
  for k, v in d:
    line = "{}: {}\t{}: {}\n".format(k_name, k, v_name, v) # TODO handle empty labels
    result_msg += line
  return result_msg

@bot.command()
async def alltags(ctx):
  to_send = "```\n" + pretty_print_dict(tag_usage.most_common(), "tag", "freq") + "```"
  await ctx.send(to_send)

@bot.command()
async def msgtags(ctx, msg: MyPartialMessageConverter):
  to_send = "```\n" + pretty_print_list(msg_tags[msg]) + "```"
  await ctx.send(to_send)

@bot.command()
async def search(ctx, *tags: str): # ignores nonexistnt tags
  # bot.clean() # shd cln at sm pnt bt nt sure whn or how
  result = set.intersection(*[tag_msgs[tag] for tag in tags if tag in tag_msgs])
  result = [msg.jump_url for msg in result]  
  print(result)
  to_send = pretty_print_list(result)
  await ctx.send(to_send)

@bot.command() # debugging
async def getid(ctx):
  print(await ctx.history(limit = 2).next())

#################################################

password = os.environ['password']
bot.run(password)
