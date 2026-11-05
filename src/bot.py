import discord
import os
import asyncio
from dotenv import load_dotenv
from lichess import *
from discord.ext import commands
from discord import app_commands
from stats import *

load_dotenv()
token = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="$", intents=intents)

async def startup():
    await bot.tree.sync()

bot.setup_hook = startup

@app_commands.choices(
    color=[
        app_commands.Choice(name="White", value="white"),
        app_commands.Choice(name="Black", value="black")
    ],
    format=[
        app_commands.Choice(name="Rapid", value="rapid"),
        app_commands.Choice(name="Blitz", value="blitz"),
        app_commands.Choice(name="Classical", value="classical"),
        app_commands.Choice(name="Bullet", value="bullet"),
        app_commands.Choice(name="Ultrabullet", value="ultrabullet"),
        app_commands.Choice(name="Correspondence", value="correspondence")
    ],
    variant=[
        app_commands.Choice(name="Standard", value="standard")
    ],
    result=[
        app_commands.Choice(name="Win", value="win"),
        app_commands.Choice(name="Loss", value="loss"),
        app_commands.Choice(name="Draw", value="draw")
    ],
    mode=[
        app_commands.Choice(name="All", value="all"),
        app_commands.Choice(name="Rated", value="rated"),
        app_commands.Choice(name="Unrated", value="unrated")
    ]
)
@bot.tree.command(name="chess", description="Look up Lichess statistics")
async def chess(
    interaction: discord.Interaction,
    username: str,
    color: str = "white",
    format: str = "rapid",
    variant: str = "standard",
    result: str = "win",
    mode: str = "all"
):
    await interaction.response.defer(thinking=True)

    count = await asyncio.to_thread(
        win_loss_draw_stats, username, color, format, variant, result, mode
    )

    if isinstance(count, str):
        await interaction.followup.send(count)
        return

    await interaction.followup.send(
        f"{username}: {count} {result}(s) as {color} in {format}"
    )

@bot.tree.command(name="puzzles", description="Look up Lichess puzzle statistics")
async def puzzles(interaction: discord.Interaction, username: str):
    await interaction.response.defer(thinking=True)

    stats = await asyncio.to_thread(get_puzzle_stats, username)

    rating, games_played = stats

    await interaction.followup.send(
        f"{username}'s puzzle rating: {rating}\n"
        f"Puzzles played: {games_played}"
    )

    
bot.run(token)
