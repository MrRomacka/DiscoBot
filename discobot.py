import discord
import requests
from googletrans import Translator
import asyncio
import wikipedia

TOKEN = 'Unknown for now'

class QuakeReq():
    def __init__(self, name):
        qc_req = requests.get(f'https://quake-stats.bethesda.net/api/v2/Player/Stats?name={name}')
        if qc_req.status_code == 500:
            self.status_code = 500
        else:
            self.status_code = 200
            self.name = qc_req.json()['name']

            self.duel = qc_req.json()["playerRatings"]["duel"]
            self.duel_rating = self.duel['rating']
            self.duel_deviation = self.duel["deviation"]
            self.duel_gamescount = self.duel["gamesCount"]
            self.duel_last_update = self.duel['lastChange']

            self.tdm = qc_req.json()["playerRatings"]["tdm"]
            self.tdm_rating = self.tdm['rating']
            self.tdm_deviation = self.tdm["deviation"]
            self.tdm_gamescount = self.tdm["gamesCount"]
            self.tdm_last_update = self.tdm['lastChange']

    def full_info(self):
        if self.status_code == 500:
            print('Invalid nickname, try another one')
        else:
            return (f'Name: {self.name}\n \n'
                    f'Duel: {self.duel_rating}±{self.duel_deviation} (Games: {self.duel_gamescount})\n'
                    f'2v2 TDM: {self.tdm_rating}±{self.duel_deviation} (Games: {self.tdm_gamescount})')

class WeatherReq():
    def __init__(self, city):
        self.API = '2c6c62ecc0d20abf473f5b3274545e06'
        self.req = requests.get(f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={self.API}')

    def m_info(self):
        if self.req.status_code == 500:
            return 'Wrong city name or something else'
        else:
            wth = self.req.json()
            print(wth)
            return (f'{wth["name"]}, {wth["sys"]["country"]}: ' \
                    f'{wth["main"]["temp"]}*F, {wth["weather"][0]["main"]}')


class DisBot(discord.Client):
    async def on_ready(self):
        print(f'{self.user} подключён к Discord!')
        for guild in client.guilds:
            print(
                f'{client.user} подключился к тусе:\n'
                f'{guild.name} (id: {guild.id})'
            )
        self.ln_src = 'ru'
        self.ln_dest = 'en'

    async def on_message(self, message):
        if message.author == self.user:
            return
        if 'кот' in message.content.lower():
            res = requests.get('https://api.thecatapi.com/v1/images/search')
            await message.channel.send(res.json()[0]['url'])
        if 'собака' in message.content.lower():
            res = requests.get('https://dog.ceo/api/breeds/image/random')
            await message.channel.send(res.json()['message'])
        if message.content.lower() == '!help':
            await message.channel.send('''List of commands:
*!help* - command list
*!qcs {name}* - general stats from Quake Champions
*!wth {city}* - current weather
*!trans/!text* - translation from {src} to {dest}
*!change* - changing source/destination pair
*!set_timer {time in hours} hours {time in minutes} minutes* - setting timer
*!wikipage {title}* - showing first in search Wikipedia page
*!wikilang {lang}* - changing Wikipedia language
            \nOther funcs may be in dev
                '''
                )
        if message.content.startswith('!trans'):
            needtotr = message.content[6:]
            translator = Translator()
            translated_one = translator.translate(needtotr, dest='ru').text
            await message.channel.send(translated_one)
        if message.content.startswith('!change'):
            self.ln_src = message.content[8:10]
            self.ln_dest = message.content[11:13]
            await message.channel.send(f'{self.ln_src}-{self.ln_dest} are chosen')
        if message.content.startswith('!text'):
            needtotr = message.content[5:]
            translator = Translator()
            translated_one = translator.translate(needtotr, src=self.ln_src, dest=self.ln_dest).text
            await message.channel.send(translated_one)
        if message.content.lower().startswith('!set_timer'):
            hours, minutes = int(message.content.split()[2]), int(message.content.split()[4])
            await message.channel.send(f'Timer set for {hours} hours and {minutes} minutes')
            await asyncio.sleep(hours * 3600 + minutes * 60)
            await message.channel.send('YOUR TIME HAS COME :alarm_clock:')
        if message.content.lower().startswith('!qcs'):
            qcs = QuakeReq(message.content[5:])
            await message.channel.send(qcs.full_info())
        if message.content.lower().startswith('!wth'):
            wth = WeatherReq(message.content[5:])
            await message.channel.send(wth.m_info())
        if message.content.lower().startswith('!wikilang'):
            wikipedia.set_lang(message.content.lower()[10:])
        if message.content.lower().startswith('!wikipage'):
            pg = wikipedia.page(wikipedia.search(message.content.lower()[10:])[0])
            await message.channel.send(f'{pg.title}\n{pg.content[:400]}\n\n{pg.url}')


client = DisBot()
client.run(TOKEN)
