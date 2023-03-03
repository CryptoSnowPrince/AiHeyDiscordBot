import discord
import os
import requests
import asyncio
import keyboards
import string
import time
import replicate
import urllib.request
from dotenv import dotenv_values
from PIL import Image, ImageDraw, ImageFont
import numpy as np

import myconfig
import messages
config = dotenv_values(".env")

os.environ['REPLICATE_API_TOKEN'] = config['REPLICATE_API_TOKEN']

replicate_token = config['REPLICATE_TOKEN']

client = discord.Client(intents=discord.Intents.all())
PREFIX = "/hey"


@client.event
async def on_ready():
    # for guild in client.guilds:
    #     if guild.name == config("DISCORD_GUILD"):
    #         break
    # print(
    #     f'{client.user} is connected to the following guild:\n'
    #     f'{guild.name}(id: {guild.id})'
    # )
    pass


@client.event
async def on_message(message):

    # for guild in client.guilds:
    #     if guild.name == config("DISCORD_GUILD"):
    #         break

    if message.author == client.user:
        return

    if message.content.startswith(PREFIX + " "):
        await handle_input(message)


async def handle_input(message):
    prompt = message.content.split(PREFIX + " ")[1]
    if prompt.strip() == "":
        return

    username = message.author.id
    origin_username = username if username else "none"
    # if not username:
    #     username = str(time.time)

    # if username in comps.keys() and (time.time() - comps[username]) < 40:
    #     await pending(message, username, origin_username)
    #     return
    # comps[username] = time.time()
    model = replicate.models.get("stability-ai/stable-diffusion")

    version = model.versions.get(
        "db21e45d3f7023abc2a46ee38a23973f6dce16bb082a930b0c49861f96d1e5bf")

    # https://replicate.com/stability-ai/stable-diffusion/versions/f178fa7a1ae43a9a9af01b833b9d2ecf97b1bcb0acfd2dc5dd04895e042863f1#input
    inputs = {
        'width': 768,
        'height': 768,
        'prompt_strength': 0.8,
        'num_outputs': 1,
        'num_inference_steps': 50,
        'guidance_scale': 7.5,
        'scheduler': "DPMSolverMultistep",
    }
    inputs['prompt'] = prompt
    wait_m = await message.channel.send(messages.message["/wait"])
    prediction = replicate.predictions.create(version=version, input=inputs)
    tm = 40
    output = []
    old_percent_m = ""
    while tm > 0:
        prediction.reload()
        print(prediction.status)
        if prediction.status == "failed":
            break
        print(prediction.logs)
        percent = 0
        if prediction.logs:
            percent = prediction.logs.split("\n")[-1].split("|")[0]

        percent_m = ""
        if percent:
            percent_m = percent

        if percent_m != old_percent_m:
            # await wait_m.edit_text("Processing request from @" + origin_username + " | " + prompt + " | " + percent_m)
            pass
        old_percent_m = percent_m
        if prediction.status == 'succeeded':
            output = prediction.output
            break
        await asyncio.sleep(5)
        tm -= 5

    if len(output) == 0:
        # await wait_m.edit_text("Try running it again, or try a different prompt")
        return
    generated_image_url = output[0]
    tick = time.time()
    water_mark(generated_image_url, username)
    photo = open(f"images/{username}_watermarked.png", "rb")
    await wait_m.delete()
    Buy = "https://pancakeswap.finance/swap"
    Telegram = "https://t.me/AiHeyOfficial"
    Website = "https://aihey.co"
    Telegram_text = "Join AiHey"
    Website_text = "Website"
    Buy_text = "BUY IMAGE"
    SPACE = "    "
    authorLink = f"https://discordapp.com/users/{message.author.id}"
    caption = f"{prompt}\nAn Image Generated by [@{message.author}]({authorLink}) *\n\n"
    embed = discord.Embed(title=f"{prompt}\nAn Image Generated by @{message.author} *\n\n", description=(
        f"`>` [{Telegram_text}]({Telegram}){SPACE}"
        f"`>` [{Website_text}]({Website}){SPACE}"
        f"`>` [{Buy_text}]({Buy})"
    ), color=9699539)
    embed.set_author(
        name=f"{message.author}",
    )
    embed.set_footer(
        text="AiHey Footer",
        # icon_url="file://aihey_watermark.png",
    )
    file = discord.File(photo, 'image.jpg')
    embed.set_image(url=f"attachment://images/{username}_watermarked.png")
    embed.set_thumbnail(url=f"attachment://images/{username}_watermarked.png")

    await message.channel.send(file=file, embed=embed)


def water_mark(image_url, username):
    urllib.request.urlretrieve(image_url, f"images/{username}.png")
    im = Image.open(f"images/{username}.png").convert("RGBA")
    water_mark = Image.open("aihey_watermark.png").convert("RGBA")
    alpha = water_mark.split()[-1]
    alpha = alpha.point(lambda p: int(float(p)/1.5))
    water_mark.putalpha(alpha)
    water_mark_width, water_mark_height = water_mark.size
    width, height = im.size

    watermark_im = Image.new('RGBA', im.size, color=(0, 0, 0, 0))
    watermark_im.paste(
        water_mark, (width-water_mark_width, height-water_mark_height))

    watermark_im = Image.alpha_composite(im, watermark_im)
    watermark_im.save(f"images/{username}_watermarked.png")


client.run(config['TOKEN'])
