import os
import discord
from discord.ext import commands
from discord import app_commands

import config
from database import Database
from modules.all_features import setup


# ==============================
# ПРОВЕРКА ПЕРЕМЕННЫХ ОКРУЖЕНИЯ
# ==============================

env_token = os.getenv("BOT_TOKEN", "").strip()

if env_token:
    config.BOT_TOKEN = env_token

print("====================================")
print("KVAZAR • Kvazarchik")
print("====================================")
print("BOT_TOKEN найден:", bool(config.BOT_TOKEN))

if not config.BOT_TOKEN:
    print("ERROR: BOT_TOKEN не найден!")
    print("Добавь переменную окружения BOT_TOKEN на хосте.")
    raise SystemExit(1)


# ==============================
# BOT
# ==============================

class KvazarBot(commands.Bot):

    def __init__(self):
        intents = discord.Intents.default()

        intents.members = True
        intents.message_content = True
        intents.guilds = True
        intents.messages = True
        intents.voice_states = True

        super().__init__(
            command_prefix=config.PREFIX,
            intents=intents,
            help_command=None
        )

        self.db = Database()

    async def setup_hook(self):
        print("INFO: Подключение к базе данных...")

        await self.db.connect()

        print("INFO: Загрузка модулей...")

        await setup(self)

        print("INFO: Синхронизация slash-команд...")

        guild = discord.Object(id=config.GUILD_ID)

        self.tree.copy_global_to(guild=guild)

        await self.tree.sync(guild=guild)

        self.added = True

        print("INFO: Slash-команды синхронизированы.")


    async def on_ready(self):
        print("------------------------------------")
        print(f"INFO: Бот запущен: {self.user}")
        print(f"INFO: ID: {self.user.id}")
        print(f"INFO: Серверов: {len(self.guilds)}")
        print("------------------------------------")

        await self.change_presence(
            activity=discord.Game(
                name="KVAZAR • /help"
            )
        )


    async def close(self):
        try:
            await self.db.close()
        except Exception as e:
            print("WARNING: Ошибка закрытия БД:", repr(e))

        await super().close()


# ==============================
# CREATE BOT
# ==============================

bot = KvazarBot()


# ==============================
# SLASH COMMAND ERRORS
# ==============================

@bot.tree.error
async def on_app_error(interaction, error):

    if isinstance(error, app_commands.CheckFailure):
        msg = "⛔ У тебя нет прав для этой команды."

    elif isinstance(error, app_commands.CommandOnCooldown):
        msg = f"⏳ Подожди {error.retry_after:.1f} сек."

    else:
        print("COMMAND ERROR:", repr(error))
        msg = "❌ Произошла ошибка. Проверь консоль Bothost."

    try:
        if interaction.response.is_done():
            await interaction.followup.send(
                msg,
                ephemeral=True
            )
        else:
            await interaction.response.send_message(
                msg,
                ephemeral=True
            )

    except Exception:
        pass


# ==============================
# START
# ==============================

if __name__ == "__main__":

    print("INFO: Запуск Kvazarchik...")

    try:
        bot.run(config.BOT_TOKEN)

    except discord.LoginFailure:
        print("ERROR: Discord отклонил BOT_TOKEN.")
        print("Проверь, что на хосте указан НОВЫЙ токен бота.")
        raise

    except Exception as e:
        print("ERROR: Бот завершился с ошибкой:")
        print(repr(e))
        raise
