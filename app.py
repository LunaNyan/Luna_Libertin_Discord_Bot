#!/usr/bin/python3
import discord
import asyncio
import logging

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='log.txt', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

client = discord.Client()

#Strings
bot_ver = '1.0.0'

help_source = 'https://github.com/LunaNyan/Luna_Libertin_Discord_Bot\n'
help_source+= '```This code can be used under MIT License.\n'
help_source+= 'type `~license` to view license announcement.\n'
help_source+= 'and also feel free to fork or creating issue.```'

bot_invite_url = 'https://discordapp.com/oauth2/authorize?client_id=502305122404007956&scope=bot'

#일체형으로 작성해야 하기에 라이센스 전문을 하드코딩합니다
license = '```MIT License\n\n'
license+= 'Copyright (c) 2018 ItsLunaNyan\n\n'
license+= 'Permission is hereby granted, free of charge, to any person obtaining a copy\n'
license+= 'of this software and associated documentation files (the "Software"), to deal\n'
license+= 'in the Software without restriction, including without limitation the rights\n'
license+= 'to use, copy, modify, merge, publish, distribute, sublicense, and/or sell\n'
license+= 'copies of the Software, and to permit persons to whom the Software is\n'
license+= 'furnished to do so, subject to the following conditions:\n\n'
license+= 'The above copyright notice and this permission notice shall be included in all\n'
license+= 'copies or substantial portions of the Software.\n\n'
license+= 'THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR\n'
license+= 'IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,\n'
license+= 'FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE\n'
license+= 'AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER\n'
license+= 'LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,\n'
license+= 'OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE\n'
license+= 'SOFTWARE.```'

help = '```~repo : show repository to this project\n'
help+= '~license : show MIT license announcement\n'
help+= '~help : show this help```'

@client.event
async def on_ready():
    print('name : ' + client.user.name)
    print('id   : ' + client.user.id)
    await client.change_presence(game=discord.Game(name='testing'))

@client.event
async def on_message(message):
    if message.content.startswith('~help'):
        await client.send_message(message.channel, help)
    elif message.content.startswith('~license'):
        await client.send_message(message.channel, license)
    elif message.content.startswith('~repo'):
        await client.send_message(message.channel, help_source)

# 토큰은 여기다 싸질러주세요
client.run('')
