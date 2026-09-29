import discord
from discord.ext import commands
from discord import app_commands
import config
from database import Database
from modules.all_features import setup

class KvazarBot(commands.Bot):
    def __init__(self):
        intents=discord.Intents.default()
        intents.members=True
        intents.message_content=True
        intents.guilds=True
        intents.messages=True
        intents.voice_states=True
        super().__init__(command_prefix=config.PREFIX,intents=intents,help_command=None)
        self.db=Database()
    async def setup_hook(self):
        await self.db.connect()
        await setup(self)
        guild=discord.Object(id=config.GUILD_ID)
        self.tree.copy_global_to(guild=guild)
        await self.tree.sync(guild=guild)
        self.added=True
    async def on_ready(self):
        await self.change_presence(activity=discord.Game(name='KVAZAR • /help'))
        print(f'Logged in as {self.user} | Guilds: {len(self.guilds)}')
    async def close(self):
        await self.db.close(); await super().close()

bot=KvazarBot()

@bot.tree.error
async def on_app_error(interaction,error):
    if isinstance(error,app_commands.CheckFailure): msg='⛔ У тебя нет прав для этой команды.'
    elif isinstance(error,app_commands.CommandOnCooldown): msg=f'⏳ Подожди {error.retry_after:.1f} сек.'
    else:
        print('COMMAND ERROR:',repr(error)); msg='❌ Произошла ошибка. Проверь консоль Bothost.'
    try:
        if interaction.response.is_done(): await interaction.followup.send(msg,ephemeral=True)
        else: await interaction.response.send_message(msg,ephemeral=True)
    except: pass

if __name__=='__main__':
    if not config.BOT_TOKEN or config.BOT_TOKEN.startswith('PASTE_'):
        raise SystemExit('В config.py вставь BOT_TOKEN')
    bot.run(config.BOT_TOKEN)
