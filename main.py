# IMPORTING DISCORD.PY, AS IT ALLOWS ACCESS TO DISCORD'S API.
import discord
import discord
import os
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
from dotenv import load_dotenv
from discord.ext import commands
import json
from openai import OpenAI

# Load the .env file that contains the bot token
load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
print(OPENAI_API_KEY)
client = OpenAI(
  api_key = OPENAI_API_KEY
)

# Initialize the bot with command prefix
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

# Load the FPL data once the bot is ready
@bot.event
async def on_ready():
    global elements_df, gk_data, Defender_data, midfielder_data, forward_data
    with open('C:/Users/Ganesh/Documents/FPL/FPL_Data.json', encoding='utf-8') as f:
        data = json.load(f)
    
    elements_df = pd.DataFrame(data['elements'])

    gk_data = elements_df[elements_df['element_type'] == 1]
    Defender_data = elements_df[elements_df['element_type'] == 2]
    midfielder_data = elements_df[elements_df['element_type'] == 3]
    forward_data = elements_df[elements_df['element_type'] == 4]

    print(f'{bot.user.name} has connected to Discord!')
# Command to get top 20 goalkeepers
@bot.command(name='topgks')
async def top_goalkeepers(ctx):
    top_20_selected_gks = gk_data.copy()
    top_20_selected_gks['selected_by_percent'] = top_20_selected_gks['selected_by_percent'].astype(float)
    top_20_selected_gks = top_20_selected_gks.sort_values(by='selected_by_percent', ascending=False)
    top_20_selected_gks['name'] = top_20_selected_gks['first_name'] + ' ' + top_20_selected_gks['second_name']
    top_20_selected_gks = top_20_selected_gks.head(20)[['name', 'now_cost', 'points_per_game', 'total_points', 'clean_sheets']]

    # Convert to string for Discord message
    response = top_20_selected_gks.to_string(index=False)
    await ctx.send(f"```{response}```")

# Command to get top 20 defenders
@bot.command(name='topdefs')
async def top_defenders(ctx):
    top_20_selected_def = Defender_data.copy()
    top_20_selected_def['selected_by_percent'] = top_20_selected_def['selected_by_percent'].astype(float)
    top_20_selected_def = top_20_selected_def.sort_values(by='selected_by_percent', ascending=False)
    top_20_selected_def['name'] = top_20_selected_def['first_name'] + ' ' + top_20_selected_def['second_name']
    top_20_selected_def = top_20_selected_def.head(20)[['name', 'now_cost', 'points_per_game', 'total_points', 'clean_sheets']]

    # Convert to string for Discord message
    response = top_20_selected_def.to_string(index=False)
    await ctx.send(f"```{response}```")

# Command to get top 20 mid fielders
@bot.command(name='topmids')
async def top_midfielders(ctx):
    top_20_selected_mid = midfielder_data.copy()
    top_20_selected_mid['selected_by_percent'] = top_20_selected_mid['selected_by_percent'].astype(float)
    top_20_selected_mid = top_20_selected_mid.sort_values(by='selected_by_percent', ascending=False)
    top_20_selected_mid['name'] = top_20_selected_mid['first_name'] + ' ' + top_20_selected_mid['second_name']
    top_20_selected_mid = top_20_selected_mid.head(20)[['name', 'now_cost', 'points_per_game', 'total_points', 'clean_sheets', 'goals_scored','assists']]

    # Convert to string for Discord message
    response = top_20_selected_mid.to_string(index=False)
    await ctx.send(f"```{response}```")

# Command to get top 20 Forwards
@bot.command(name='topfwds')
async def top_forwards(ctx):
    top_20_selected_fwd = forward_data.copy()
    top_20_selected_fwd['selected_by_percent'] = top_20_selected_fwd['selected_by_percent'].astype(float)
    top_20_selected_fwd = top_20_selected_fwd.sort_values(by='selected_by_percent', ascending=False)
    top_20_selected_fwd['name'] = top_20_selected_fwd['first_name'] + ' ' + top_20_selected_fwd['second_name']
    top_20_selected_fwd = top_20_selected_fwd.head(20)[['name', 'now_cost', 'points_per_game', 'total_points', 'goals_scored','assists']]

    # Convert to string for Discord message
    response = top_20_selected_fwd.to_string(index=False)
    await ctx.send(f"```{response}```")

@bot.command(name='topgks_img')
async def top_goalkeepers_img(ctx):
    top_20_selected_gks = gk_data.copy()
    top_20_selected_gks['selected_by_percent'] = top_20_selected_gks['selected_by_percent'].astype(float)
    top_20_selected_gks = top_20_selected_gks.sort_values(by='selected_by_percent', ascending=False)
    top_20_selected_gks['name'] = top_20_selected_gks['first_name'] + ' ' + top_20_selected_gks['second_name']
    top_20_selected_gks = top_20_selected_gks.head(20)[['name', 'now_cost', 'points_per_game', 'total_points', 'clean_sheets']]

    # Create a plot or table as an image
    plt.figure(figsize=(12, 8))
    plt.axis('tight')
    plt.axis('off')
    plt.table(cellText=top_20_selected_gks.values, colLabels=top_20_selected_gks.columns, cellLoc='center', loc='center')

    # Save to a BytesIO object
    img_data = BytesIO()
    plt.savefig(img_data, format='png', bbox_inches='tight', dpi=300)
    img_data.seek(0)

    # Send the image
    await ctx.send(file=discord.File(fp=img_data, filename='top_goalkeepers.png'))

@bot.command(name='topmids_img')
async def top_midfielders_img(ctx):
    top_20_selected_mid = midfielder_data.copy()
    top_20_selected_mid['selected_by_percent'] = top_20_selected_mid['selected_by_percent'].astype(float)
    top_20_selected_mid = top_20_selected_mid.sort_values(by='selected_by_percent', ascending=False)
    top_20_selected_mid['name'] = top_20_selected_mid['first_name'] + ' ' + top_20_selected_mid['second_name']
    top_20_selected_mid = top_20_selected_mid.head(20)[['name', 'now_cost', 'points_per_game', 'total_points', 'clean_sheets','goals_scored','assists']]

    # Create a plot or table as an image
    plt.figure(figsize=(12, 8))
    plt.axis('tight')
    plt.axis('off')
    plt.table(cellText=top_20_selected_mid.values, colLabels=top_20_selected_mid.columns, cellLoc='center', loc='center')

    # Save to a BytesIO object
    img_data = BytesIO()
    plt.savefig(img_data, format='png', bbox_inches='tight', dpi=300)
    img_data.seek(0)

    # Send the image
    await ctx.send(file=discord.File(fp=img_data, filename='top_goalkeepers.png'))

# # EVENT LISTENER FOR WHEN A NEW MESSAGE IS SENT TO A CHANNEL.
@bot.event
async def on_message(message):

    if message.author == bot.user:
        return
    if message.guild:
        print(f"Received a message from {message.guild.name} in {message.channel.name}: {message.content}")
    else:
        print(f"Received a direct message: {message.content}")
    # CHECKS IF THE MESSAGE THAT WAS SENT IS EQUAL TO hello.
    if message.content:
        print(f"Message content: '{message.content}'")  # Debugging line to check the content

        # Compare the content to "hello"
        if message.content.lower() == "hello":
            print("Detected 'hello' message, sending response...")  # Debugging line
            await message.channel.send("hey ganiman_'s FPL Server user")
        elif message.content.lower() == "you":
            print("Detected 'you' message, sending response...")  # Debugging line
            await message.channel.send("i am also good")
        elif message.content.lower() == "dengei":
            print("Detected 'you' message, sending response...")  # Debugging line
            await message.channel.send("Nuvve Dengei")
        else:
            completion = client.chat.completions.create(
                model='gpt-3.5-turbo',
                # prompt=message.content,
            # print(completion.choices[0].text)
            
            # response = openai.ChatCompletion.create(
            #     model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": message.content}
                ]
            )

            # Send the response back to the Discord channel
            await message.channel.send(completion.choices[0].message.content)
    else:
        print("Received an empty message.")
        # await message.channel.send("I don't know how to respond to that")

@bot.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, welcome to my Discord server!'
    )


# EXECUTES THE BOT WITH THE SPECIFIED TOKEN. TOKEN HAS BEEN REMOVED AND USED JUST AS AN EXAMPLE.
bot.run(DISCORD_TOKEN)