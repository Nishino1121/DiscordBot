import discord
import os
from keep_alive import keep_alive
intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True
intents.guilds = True

client = discord.Client(intents=intents)
excluded_channels = os.getenv("EXCLUDED_CHANNELS")
if excluded_channels is None:
    excluded_channels = []
else:
    excluded_channels = [int(x) for x in excluded_channels.split(',')]

@client.event
async def on_ready():
    print('ログインしました')


@client.event
async def on_voice_state_update(member, before, after):
    channel_name = "入退室ログ"  # 通知したいチャンネルの名前
    channel = discord.utils.get(member.guild.channels, name=channel_name)

    if before.channel != after.channel:  # チャンネルが変わった
        if before.channel is None:  # ボイスチャンネルに入った
            if after.channel.id not in excluded_channels:
                await channel.send(f'{member.name} が {after.channel.name} に参加しました。')
        elif after.channel is None:  # ボイスチャンネルから出た
            if before.channel.id not in excluded_channels:
                await channel.send(f'{member.name} が {before.channel.name} から退出しました。')
        else:  # ボイスチャンネルを移動した
            if before.channel.id not in excluded_channels:
                await channel.send(f'{member.name} が {before.channel.name} から退出しました。')
            if after.channel.id not in excluded_channels:
                await channel.send(f'{member.name} が {after.channel.name} に参加しました。')

TOKEN = os.getenv("DISCORD_TOKEN")
# Web サーバの立ち上げ
keep_alive()
client.run(TOKEN)
