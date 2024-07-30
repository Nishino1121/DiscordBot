import discord
import os
from keep_alive import keep_alive
intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True
intents.guilds = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print('ログインしました')


@client.event
async def on_voice_state_update(member, before, after):
    channel_name = "入退室ログ"  # 通知したいチャンネルの名前
    channel = discord.utils.get(member.guild.channels, name=channel_name)

    if before.channel is None and after.channel is not None:  # ボイスチャンネルに入った
        await channel.send(f'{member.name} が {after.channel.name} に参加しました。')
    elif before.channel is not None and after.channel is None:  # ボイスチャンネルから出た
        await channel.send(f'{member.name} が {before.channel.name} から退出しました。')

TOKEN = os.getenv("DISCORD_TOKEN")
# Web サーバの立ち上げ
keep_alive()
client.run(TOKEN)
