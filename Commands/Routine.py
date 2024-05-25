"""
    間隔一段時間執行命令 Routine Function
"""
import discord as dc
from discord.ext import commands
from discord.ext import tasks
import os
from Core import Cog_Extension

import urllib.request as req
import bs4
import os
import json
from datetime import datetime

CWB_LIMIT = 100
SHOW_DATA_COLUMN = 1

CWB_earthquake_file_url = "https://www.cwb.gov.tw/V8/C/E/MOD/MAP_LIST.html?T=2022082817-2"
CWB_website = "https://www.cwb.gov.tw/V8/C/E/index.html"

global CWB_titles
global CWB_titles_new
global CWB_count                                

CWB_titles = [[' ' for i in range(7)] for j in range(CWB_LIMIT)]
CWB_titles_new = [[' ' for i in range(7)] for j in range(CWB_LIMIT)]

CWB_count = 0

now_date_time = datetime.now().strftime("%H:%M:%S")

def CWB_earthquake_crawling(array: list) -> int:

    try:
         web_request = req.Request(CWB_earthquake_file_url, headers = 
        {
            "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36"
        })

    except:

        return -1

    with req.urlopen(url = web_request) as response:
        web_data = response.read().decode("utf-8")
    
    web_fitter = bs4.BeautifulSoup(web_data, "html.parser")

    web_dot = web_fitter.find_all("a", class_ = "dot")
    web_far_dot = web_fitter.find_all("a", class_ = "far-dot")
    web_lg_dot = web_fitter.find_all("a", class_ = "dot lg-dot")

    try:
        for target in web_dot:

            data_name = str(target["data-name"])
            number = "" + data_name[3 : ]
            number = int(number)

            array[number - 1][0] = str(number)
            array[number - 1][1] = str(target.text)
    except:
        pass

    try:
        for target in web_far_dot:
            
            data_name = str(target["data-name"])
            number = "" + data_name[3 : ]
            number = int(number)

            array[number - 1][0] = str(number)
            array[number - 1][1] = str(target.text)
    except:
        pass

    try:
        for target in web_lg_dot:
            
            data_name = str(target["data-name"])
            number = "" + data_name[3 : ]
            number = int(number)

            array[number - 1][0] = str(number)
            array[number - 1][1] = str(target.text)

    except:
        pass

    for i in range(0, SHOW_DATA_COLUMN, 1):
        
        words = array[i][1].split("，")

        if words[0] != "None" and words[0] != " ":
            
            array[i][2] = words[0]
            array[i][3] = words[1]
            array[i][4] = words[2]
            array[i][5] = words[3]
            array[i][6] = words[4]

    return 

def CWB_earthquake_make_embed(array: list, start: int, end : int):
            
    embed = dc.Embed(
        title = "📢 ❗❗❗ 🌋 交通部中央氣象局 最近地震 🌋 ❗❗❗",
        description = "Emergency Situations : Recent Earthquake from CWB",
        color = 0xFF5733
    )
    for i in range(0, SHOW_DATA_COLUMN, 1):

        embed.add_field(
            name = f"⌚ 地震時間：{array[i][3]}",
            value = f"\
                📍 形成地點：{array[i][4]}\n\
                🎯 影響區域：{array[i][2]}\n\
                🌋 地震規模：**{array[i][6]}**\n\
                🚩 地震深度：{array[i][5]}\n\
                📧 地震編號：({array[i][0]}) __{CWB_website}__\n\n\n\
                ",
            inline = False
        )

    return embed

def main() -> None:

    CWB_earthquake_crawling(CWB_titles)

    return

main()

class Routine(Cog_Extension):

    def __init__(self, *args):
        super().__init__(*args)

        self.detect_earthquake.start()

    @tasks.loop(seconds = 2.0)
    async def detect_earthquake(self) -> int:
        """
            Auto detects CWB currently earthquakes. (loop 2.0s)

            自動 偵測 交通部中央氣象局-最近地震 標題。
        """
        """
            Web URL = https://www.cwb.gov.tw/V8/C/E/index.html
            Document URL = https://www.cwb.gov.tw/V8/C/E/MOD/MAP_LIST.html?T=2022082817-2
            Target = HTML XHR titles
        """
        
        await self.bot.wait_until_ready()

        global CWB_titles
        global CWB_titles_new
        global CWB_count

        with open("./database.json", "r", encoding = "utf-8") as file:
            earthquake_channel = json.load(file)

        channel = self.bot.get_channel(int(earthquake_channel["earthquake_channel"][0]))
        
        """
            Function Start
        """
        
        if CWB_earthquake_crawling(CWB_titles_new) == -1:
            
            for i in range(len(earthquake_channel["earthquake_channel"])):

                channel = self.bot.get_channel(int(earthquake_channel["earthquake_channel"][i]))

                await channel.send("CWB website https connect failed.")

            return 0

        different = False

        if len(CWB_titles[0][1]) != len(CWB_titles_new[0][1]):
            different = True

        if different == False:
            
            array_len = len(CWB_titles[0][1])

            for i in range(array_len):

                if CWB_titles_new[0][1][i] != CWB_titles[0][1][i]:

                    different = True

                    break

        if different == False:
    
            if CWB_count == 0:
                CWB_count += 1

            print("robot : nothing...")

        else:

            if CWB_count > 0:

                print("robot : something is updating...")
                print(f"robot : the current time is {now_date_time}") 

                for i in range(len(earthquake_channel["earthquake_channel"])):

                    channel = self.bot.get_channel(int(earthquake_channel["earthquake_channel"][i]))

                    await channel.send(embed = CWB_earthquake_make_embed(CWB_titles_new, 0, 0))

                CWB_earthquake_crawling(CWB_titles)

                CWB_count += 1
                print(f"robot : calculate CWB_count = {CWB_count - 1}") 

def setup(bot):
    bot.add_cog(Routine(bot))