import discord
from discord.ext import commands
from datetime import datetime
from difflib import get_close_matches
import json
import os

TOKEN =os.getenv('TOKEN')
SERVERNAME = ''
# Set up intents
# Set up intents
intents = discord.Intents.default()
intents.message_content = True  # Enable the intents for reading message content

# Set up the bot with a command prefix and the required intents
bot = commands.Bot(command_prefix="!", intents=intents)

# load json
with open("working_data.json", "r") as file:
    tools_data = json.load(file)


tool_data = {key.lower(): value for key, value in tools_data.items()}

# Sample data structure for tool info


@bot.command(name="craft", aliases=["make", "build"])
async def craft(ctx, *args):
    # Ensure at least one argument is provided
    if len(args) == 0:
        response = (
            "Please provide the name of a tool to get information about it.\n"
            "Usage: `!craft <tool_name> [amount]`\n"
            "Example: `!craft hatchet 2`"
        )
        await ctx.send(response)
        return

    # Extract tool name and amount
    *tool_name_parts, amount = args  # Splits arguments into tool name and amount
    tool_name = " ".join(tool_name_parts).lower()

    # Check if the amount is valid; default to 1 if not provided
    try:
        amount = int(amount)
        if amount < 1:
            await ctx.send("The amount must be a positive integer.")
            return
    except ValueError:
        # If amount is not a valid number, assume it's part of the tool name
        tool_name = " ".join(args).lower()
        amount = 1
    print(tool_name)
    # Look up the tool in the tool_data dictionary
    if tool_name in tool_data:
        print("name",tool_name)
        print("data",tool_data)
        tool = tool_data[tool_name]
        print(tool)
        materials = ", ".join(
            f"{qty * amount} {name}" for name, qty in tool["materials"].items()
        )
        response = (
            f"**{tool_name.capitalize()}**\n"
            f"`Crafting Requirements for \n{amount} {tool_name}: {materials}\n"
            f"Workbench Level Required: {tool['workbench']}`"
        )
    else:
        possible_tools = get_close_matches(tool_name, tool_data.keys(), n=3, cutoff=0.6)
        if possible_tools:
            suggestions = ", ".join(possible_tools)
            response = f"Tool '{tool_name}' not found. Did you mean: {suggestions}?"
        else:
            response = (
                f"Sorry, I couldn't find any information for '{tool_name}'. "
                f"Please double-check the tool name or try another one!"
            )

    await ctx.send(response)
bot.run(TOKEN)
