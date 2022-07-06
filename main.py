#!/usr/bin/python3

import asyncio
import datetime
from asyncio import sleep

import requests
from fake_headers import Headers
from pygame import mixer


class IkeaCheck:
    period = 60
    url = 'https://www.ikea.com/ru/ru/customer-service/contact-us/zayavka-na-oformlenie-zakaza-pub1a73c1b0'
    header = Headers(
        browser="chrome",
        os="win",
        headers=True
    )
    sirena = 'sirena-vozdushnogo-naleta-26744.mp3'
    text = """В данный момент мы обрабатываем полученные заявки. Прием новых заявок запустится немного позже. Следите за обновлениями на нашем сайте."""
    mixer.init()
    mixer.music.load(sirena)

    async def verify(self) -> bool:
        r = requests.get(self.url, headers=self.header.generate())
        if r.ok:
            if self.text in r.text:
                return False
            else:
                return True
        else:
            print(f"Сайт не доступен {r.status_code}")
            return False

    async def run(self):
        while True:
            if await self.verify():
                mixer.music.play()
            else:
                print(f"Пока закрыто {datetime.datetime.now()}")
            await sleep(self.period)


if __name__ == '__main__':
    ik = IkeaCheck()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(ik.run())
