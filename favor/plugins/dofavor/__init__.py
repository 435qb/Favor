from nonebot import get_plugin_config, on_message, logger, on_command
from nonebot.plugin import PluginMetadata
from nonebot.rule import to_me, command
from nonebot.adapters import Message
from nonebot.params import EventPlainText, CommandArg, EventMessage
from .config import Config
from nonebot.adapters import Bot
from nonebot.matcher import Matcher
# from nonebot.adapters.onebot.v12 import GroupMessageDeleteEvent

import random
from .state import state

__plugin_meta__ = PluginMetadata(
    name="DoFavor",
    description="帮一下，就一下",
    usage="",
    config=Config,
)

config = get_plugin_config(Config)

logger.info(config.people)

global_state = state()
global_state.filename = config.filename

global_state.load()

@on_command("new", block=True).handle()
async def handle_new(matcher : Matcher, args: Message = CommandArg()):
    logger.debug("--- entering handle_new ---")
    logger.debug(f"text: {args.extract_plain_text()}")
    others = args.extract_plain_text().split()
    if len(others) == 0:
        return await matcher.finish("不中")
    if others[0].startswith("@"):
        others.remove(others[0])
    if len(others) != 1:
        return await matcher.finish("不中")
    
    group = others[0]
    newgroup : str = "".join(random.sample(group, k=len(group)))

    if global_state.new_group(newgroup):
        message = f"新的顺序是{newgroup[0]} {newgroup}"
    else:
        message = f"{group}已经存在，且现在是{global_state.contains(group)}"
    global_state.save()
    await matcher.finish(message)

@on_message().handle()
async def handle_ok(matcher : Matcher, args: Message = EventMessage()):
    logger.debug("--- entering handle_ok ---")
    
    others = args.extract_plain_text().split()
    if len(others) != 2 or others[0] not in config.people:
        return

    for i in others[1]:
        if i not in config.people:
            return
        
    curr = others[0]
    group = others[1]
    if len(group) < 2:
        message = f"组人太少"
    if global_state.next_group(curr, group):
        message = f"成功"
    else:
        message = f"还没组或者顺序错误"
    global_state.save()
    await matcher.finish(message)

@on_command("stat", block=True).handle()
async def handle_stat(matcher : Matcher):
    logger.debug("--- entering handle_stat ---")
    message = str(global_state) 
    if not message:
        message = "空"
    await matcher.finish(message)