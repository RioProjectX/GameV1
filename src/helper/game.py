import requests, random
from bs4 import BeautifulSoup

class GameHelper:
    def __init__(self):
        self.abs_url = "https://jawabantebakgambar.net"
        self.rel_url = "/all-answers/"

    def parse(self, html):
        return BeautifulSoup(html, "html.parser")

    def get_quest(self, ctx):
        if "cache_quest" in ctx.bot_data:
            return self.get_quest_from_cache(ctx)

        quests = self.get_quest_from_web()
        ctx.bot_data["cache_quest"] = quests

        return self.get_quest_from_cache(ctx)

    def get_quest_from_cache(self, ctx):
        index = random.randint(0, 2699)
        cache = ctx.bot_data["cache_quest"]

        return cache[index]

    def get_quest_from_web(self):
        html_content = requests.get(self.abs_url + self.rel_url).content
        body = self.parse(html_content)

        target_element = "#container > .content > #images > li:not(.clearleft)"
        elem_chunk = body.select(target_element)
        
        result = list()

        for elem in elem_chunk:
            image = self.abs_url + elem.img.get("data-src")
            answer = elem.span.text

            result.append({ "soal": image, "jawaban": answer })

        return result

game = GameHelper()
