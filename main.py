
import discord
from discord.ext import commands
import asyncio
import os
import random
import aiohttp
import json

# Bot configuration
BOT_TOKEN = "MTIzMzc3OTU0NjY5Njg0NzUzMQ.GfDQU4.J62srCJx-_Jwj8-6aXMombP_6YIggdDMOS9rAc"  # Replace with your bot token
COMMAND_PREFIX = "!"
SELECTED_GIF_URL = "https://media.giphy.com/media/sNUWF7fAUP2q4/giphy.gif"  # Direct GIF URL
DEVELOPER_CREDIT = "Developer: Syed Rehan | @9yrs"

# OpenRouter API configuration for DeepSeek
OPENROUTER_API_KEY = "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"  # Get free API key from openrouter.ai
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL_NAME = "deepseek/deepseek-r1-distill-llama-70b:free"

# Fallback responses if API fails
FALLBACK_RESPONSES = [
    "I'm having trouble connecting to my AI brain right now, but I'm still here to chat! 🤖",
    "My AI is taking a quick break, but I'd love to hear from you anyway!",
    "Technical difficulties with my smart responses, but I'm still listening! 💙",
]

# Discord bot setup
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=COMMAND_PREFIX, intents=intents)

async def get_ai_response(message_content):
    """Get response from DeepSeek R1 model via OpenRouter API"""
    if OPENROUTER_API_KEY == "YOUR_OPENROUTER_API_KEY":
        return random.choice(FALLBACK_RESPONSES)
    
    try:
        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://replit.com",
            "X-Title": "Discord Bot"
        }
        
        payload = {
            "model": MODEL_NAME,
            "messages": [
                {
                    "role": "system", 
                    "content": "You are a helpful, friendly Discord bot assistant. Keep responses concise and engaging. Be conversational and helpful."
                },
                {
                    "role": "user", 
                    "content": message_content
                }
            ],
            "max_tokens": 500,
            "temperature": 0.7
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(OPENROUTER_URL, headers=headers, json=payload, timeout=30) as response:
                if response.status == 200:
                    data = await response.json()
                    if 'choices' in data and len(data['choices']) > 0:
                        return data['choices'][0]['message']['content'].strip()
                else:
                    print(f"API Error: {response.status} - {await response.text()}")
                    return random.choice(FALLBACK_RESPONSES)
                    
    except Exception as e:
        print(f"Error calling AI API: {e}")
        return random.choice(FALLBACK_RESPONSES)

@bot.command(name='developer')
async def developer_command(ctx):
    """Show developer information"""
    embed = discord.Embed(
        title="👨‍💻 Developer Information",
        description="This bot was created by: Syed Rehan",
        color=discord.Color.magenta()
    )

    embed.add_field(
        name="🔧 Developer",
        value="**Syed Rehan**",
        inline=True
    )

    embed.add_field(
        name="📱 Contact",
        value="@9yrs",
        inline=True
    )

    embed.add_field(
        name="🤖 Bot Features",
        value="• DeepSeek R1 AI Responses\n• Custom GIF Integration\n• Discord Commands",
        inline=False
    )

    embed.add_field(
        name="🧠 AI Model",
        value="DeepSeek R1 Distill Llama 70B",
        inline=False
    )

    embed.set_image(url=SELECTED_GIF_URL)
    embed.set_footer(text=DEVELOPER_CREDIT)

    await ctx.reply(embed=embed)

@bot.event
async def on_ready():
    print(f'{bot.user} has landed!')
    print(f'Connected to {len(bot.guilds)} server(s)')
    print(f"🧠 AI Model: {MODEL_NAME}")
    print("Bot is ready to chat with DeepSeek R1!")

@bot.event
async def on_message(message):
    # Don't respond to bot's own messages
    if message.author == bot.user:
        return

    # Process commands first
    await bot.process_commands(message)

    # Only respond to direct mentions or DMs
    if bot.user.mentioned_in(message) or isinstance(message.channel, discord.DMChannel):
        async with message.channel.typing():
            # Clean the message content
            content = message.clean_content
            if bot.user.mentioned_in(message):
                content = content.replace(f'@{bot.user.display_name}', '').strip()

            if not content:
                content = "Hello!"

            # Get AI response from DeepSeek R1
            try:
                ai_response = await get_ai_response(content)

                # Create embed with AI response
                embed = discord.Embed(
                    description=ai_response,
                    color=discord.Color.blue()
                )
                embed.set_author(
                    name="DeepSeek R1 Bot",
                    icon_url=bot.user.avatar.url if bot.user.avatar else None
                )

                # Add developer credit to footer
                embed.set_footer(text=f"{DEVELOPER_CREDIT} • Powered by DeepSeek R1")

                # Always use your selected GIF
                embed.set_image(url=SELECTED_GIF_URL)

                await message.reply(embed=embed)

            except Exception as e:
                print(f"Error processing message: {e}")
                await message.reply("Oops! My AI brain had a hiccup. Please try again!")

@bot.command(name='chat')
async def chat_command(ctx, *, message: str):
    """Chat with the DeepSeek R1 AI using a command"""
    async with ctx.typing():
        try:
            ai_response = await get_ai_response(message)

            embed = discord.Embed(
                title="💬 DeepSeek R1 Response",
                description=ai_response,
                color=discord.Color.green()
            )

            # Always use your selected GIF
            embed.set_image(url=SELECTED_GIF_URL)

            # Add developer credit to footer
            embed.set_footer(text=f"{DEVELOPER_CREDIT} • Powered by DeepSeek R1")

            await ctx.reply(embed=embed)
        except Exception as e:
            await ctx.reply(f"Error: {e}")

@bot.command(name='model')
async def model_command(ctx):
    """Show current AI model information"""
    embed = discord.Embed(
        title="🧠 AI Model Information",
        description="Current AI model powering this bot:",
        color=discord.Color.purple()
    )

    embed.add_field(
        name="🤖 Model",
        value=MODEL_NAME,
        inline=False
    )

    embed.add_field(
        name="📊 Provider",
        value="OpenRouter API",
        inline=True
    )

    embed.add_field(
        name="💰 Cost",
        value="Free Tier",
        inline=True
    )

    embed.set_image(url=SELECTED_GIF_URL)
    embed.set_footer(text=DEVELOPER_CREDIT)

    await ctx.reply(embed=embed)

@bot.command(name='changegif')
async def change_gif_command(ctx, *, new_gif_url: str):
    """Change the bot's GIF (Admin only)"""
    if not ctx.author.guild_permissions.administrator:
        await ctx.reply("❌ Only administrators can change the bot's GIF!")
        return

    global SELECTED_GIF_URL
    SELECTED_GIF_URL = new_gif_url

    embed = discord.Embed(
        title="✅ GIF Updated!",
        description="The bot will now use this new GIF:",
        color=discord.Color.green()
    )
    embed.set_image(url=SELECTED_GIF_URL)
    embed.set_footer(text=DEVELOPER_CREDIT)

    await ctx.reply(embed=embed)

@bot.command(name='showgif')
async def show_gif_command(ctx):
    """Show the current GIF being used"""
    embed = discord.Embed(
        title="🎬 Current Bot GIF",
        description="This is the GIF I use in all my responses:",
        color=discord.Color.purple()
    )
    embed.set_image(url=SELECTED_GIF_URL)
    await ctx.reply(embed=embed)

@bot.command(name='info')
async def info_command(ctx):
    """Show bot help information"""
    embed = discord.Embed(
        title="🤖 DeepSeek R1 Chat Bot Help",
        description="I'm powered by DeepSeek R1 AI! Here's how to use me:",
        color=discord.Color.gold()
    )

    embed.add_field(
        name="💬 Chat with AI",
        value="• Mention me in a message: `@BotName your message`\n• DM me directly\n• Use the command: `!chat your message`",
        inline=False
    )

    embed.add_field(
        name="🎬 GIF Commands",
        value="• `!showgif` - Show current GIF\n• `!changegif [url]` - Change GIF (Admin only)\n• I use the same GIF in all responses!",
        inline=False
    )

    embed.add_field(
        name="ℹ️ Other Commands",
        value="• `!info` - Show this help message\n• `!ping` - Check bot latency\n• `!developer` - Show developer info\n• `!model` - Show AI model info",
        inline=False
    )

    # Show current GIF in help
    embed.set_image(url=SELECTED_GIF_URL)
    embed.set_footer(text=f"{DEVELOPER_CREDIT} • Powered by DeepSeek R1")

    await ctx.reply(embed=embed)

@bot.command(name='ping')
async def ping_command(ctx):
    """Check bot latency"""
    latency = round(bot.latency * 1000)
    embed = discord.Embed(
        title="🏓 Pong!",
        description=f"Bot latency: {latency}ms",
        color=discord.Color.orange()
    )
    # Also show GIF with ping
    embed.set_image(url=SELECTED_GIF_URL)
    embed.set_footer(text=f"{DEVELOPER_CREDIT} • Powered by DeepSeek R1")
    await ctx.reply(embed=embed)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.reply("Missing required argument! Check `!info` for usage.")
    elif isinstance(error, commands.CommandNotFound):
        pass  # Ignore unknown commands
    else:
        print(f"Command error: {error}")
        await ctx.reply("An error occurred while processing your command.")

# Configuration check
def check_config():
    if BOT_TOKEN == "YOUR_DISCORD_BOT_TOKEN":
        print("⚠️  Please set your Discord bot token in BOT_TOKEN variable!")
        return False

    if OPENROUTER_API_KEY == "YOUR_OPENROUTER_API_KEY":
        print("⚠️  Please set your OpenRouter API key in OPENROUTER_API_KEY variable!")
        print("   Get a free API key from https://openrouter.ai")
        print("   The bot will work with fallback responses until you add the API key.")

    return True

if __name__ == "__main__":
    print("🤖 Starting DeepSeek R1 Discord Bot...")
    print(f"🧠 AI Model: {MODEL_NAME}")
    print(f"📸 Using GIF: {SELECTED_GIF_URL}")
    print(f"👨‍💻 {DEVELOPER_CREDIT}")
    print("=" * 50)

    if not check_config():
        print("❌ Configuration incomplete. Please update the bot token and try again.")
        exit(1)

    try:
        bot.run(BOT_TOKEN)
    except Exception as e:
        print(f"❌ Failed to start bot: {e}")
        print("Make sure your bot token is correct and the bot has necessary permissions!")
