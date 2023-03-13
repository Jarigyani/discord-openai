import discord
import os
from discord.ext import commands
from dotenv import load_dotenv
import openai

load_dotenv()

TOKEN = os.environ.get("TOKEN")
openai.api_key = os.environ.get("API_KEY")


bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

messages = []


@bot.event
async def on_ready():
    print("Bot is ready.")


class TestView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.stop_button = discord.ui.Button(
            style=discord.ButtonStyle.green, emoji="⏹️"
        )
        self.stop_button.disabled = True

    async def on_timeout(self):
        self.stop_button.disabled = True
        await self.message.edit(view=self)


@bot.slash_command(name="chat", description="チャットを開始します。")
async def view_test(ctx: discord.ApplicationContext, *, message):
    global messages
    messages.append({"role": "user", "content": message})

    view = TestView()
    await ctx.interaction.response.send_message(
        content="__**"
        + ctx.author.name
        + "**__"
        + "\n"
        + message
        + "\n\n"
        + "__**ChatGPT**__".strip(),
        view=view,
    )

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
    )

    await ctx.send(response.choices[0]["message"]["content"].strip())
    messages.append(
        {
            "role": "assistant",
            "content": response.choices[0]["message"]["content"].strip(),
        }
    )


bot.run(TOKEN)
