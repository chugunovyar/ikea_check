import asyncio
import datetime
from asyncio import sleep

import requests
from fake_headers import Headers
from pygame import mixer
from requests_html import AsyncHTMLSession, HTMLSession


class IkeaCheck:
    period = 5
    url = 'https://www.ikea.com/ru/ru/customer-service/contact-us/zayavka-na-oformlenie-zakaza-pub1a73c1b0'
    header = Headers(
        browser="chrome",  # Generate only Chrome UA
        os="win",  # Generate ony Windows platform
        headers=True  # generate misc headers
    )
    sirena = 'sirena-vozdushnogo-naleta-26744.mp3'
    mixer.init()
    mixer.music.load(sirena)
    session = HTMLSession()

    async def verify(self) -> bool:
        rr = self.session.get(self.url, headers=self.header.generate())
        rr.html.render()
        r = requests.get(self.url, headers=self.header.generate())
        if r.ok:
            if 'Автор формы уже закончил сбор данных и закрыл эту форму.' in r.text:
                print(r.text)
                return False
            else:
                # return True
                return False
        else:
            print(f"Сайт не доступен {r.status_code}")
            return False

    async def run(self):
        while True:
            if await self.verify():
                ## mixer.music.play()
                pass
            else:
                print(f"Пока закрыто {datetime.datetime.now()}")
            await sleep(self.period)


if __name__ == '__main__':
    ik = IkeaCheck()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(ik.run())
