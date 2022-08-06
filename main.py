import os
import discord
import requests
import random
import time
from replit import db
from datetime import datetime, timedelta

start_time = 0

my_secret = os.environ['TOKEN']

client = discord.Client()

trigger_words = ['anime', 'waifu', 'watch', 'eventually']
anime_list = []
responses = [
    "When are you going to get to catching up on your anime?",
    "That list is only getting longer and longer...", "Catch up already!",
    "Stop wasting time and catch up on your anime.",
    "Yet again you push it off to the side...",
    "I better be your favorite waifu. >:("
]

if "respond" not in db.keys():
    db["respond"] = True


def update_ShinobuResponse(s_message):
    if "shinobu" in db.keys():
        anime_list = db["shinobu"]
        anime_list.append(s_message)
        db["shinobu"] = anime_list
    else:
        db["shinobu"] = [s_message]


def delete_anime(index):
    anime_list = db["shinobu"]
    if len(anime_list) > index:
        del anime_list[index]
        db["shinobu"] = anime_list


def time_check(sec):
    mins = sec // 60
    sec = sec % 60
    hours = mins // 60
    mins = mins % 60
    return "{0}:{1}:{2}".format(int(hours), int(mins), int())


@client.event
async def on_ready():
    #print('We have logged in as {0.user}'.format(client))
    print("Kuki Shinobu, checking in!")


@client.event
async def on_message(message):
    msg = message.content

    if message.author == client.user:
        return

    if db["respond"]:
        options = responses
        #if "shinobu" in db.keys():
        #    #options = options + db["encouragements"]
        #    options.extend(db["shinobu"])

        if any(word in msg for word in trigger_words):
            await message.channel.send(random.choice(options))
            anime_list = db["shinobu"]
            if len(anime_list) > 0:
                a = random.randint(1, 20)
                #a = 1
                if a == 1:
                    await message.channel.send(
                        "Don't let your anime list get too big.")

#Commands for the bot
#This is to add encouragements ↓
    if msg.startswith("//new"):
        s_message = msg.split("//new ", 1)[1]
        update_ShinobuResponse(s_message)
        await message.channel.send(
            "Ok, fine, I'll add another anime to your list.")


#This is to delete encouragements that we have added ↓
    if msg.startswith("//del"):
        anime_list = db["shinobu"]
        if "shinobu" in db.keys():
            if len(anime_list) == 0:
                await message.channel.send(
                    "There's nothing to delete, you should know better.")
            elif len(anime_list) > 0:
                await message.channel.send(
                    "Finally, took you long enough. I was getting bored waiting for you to finish your anime."
                )
            index = int(msg.split("//del ", 1)[1])
            delete_anime(index)
            anime_list = db["shinobu"]

        await message.channel.send(anime_list)

    #This is to print out the list of encouragements that we have added ↓
    if msg.startswith("//list"):
        anime_list = []
        if "shinobu" in db.keys():
            anime_list = db["shinobu"]
        await message.channel.send(anime_list)

    #This is to turn it off and on ↓
    if msg.startswith("//respond"):
        value = msg.split("//respond ", 1)[1]
        if value.lower() == "true":
            db["respond"] = True
            await message.channel.send(
                "Better not change your mind about this later.")
        else:
            db["respond"] = False
            await message.channel.send("Fine, I'll be quiet for now.")

client.run(my_secret)
