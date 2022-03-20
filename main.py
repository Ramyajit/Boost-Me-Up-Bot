import discord
import os
import requests
import json
import random
from replit import db
#from keep_alive import keep_alive

client = discord.Client()

words = ["sad", "depressed", "unhappy", "angry", "miserable", "depressing","melancholy","gloomy","down"]

dummy_quotes = [
  "You have got this",
  "Hang in there!",
  "You are awesome",
  "Take a break, you earned it!",
  "Get yourself a dessert you deserve it!",
  "You have always got a friend in me"
]



def fetch_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " -- " + json_data[0]['a']
  return(quote)


@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return

  msg = message.content

  if msg.startswith('$hello'):
    await message.channel.send("Aloha!")

  if msg.startswith('$zen'):
    quote = fetch_quote()
    await message.channel.send(quote)

  if any(word in msg for word in words):
    await message.channel.send(random.choice(dummy_quotes))



  

  
client.run(os.environ['token'])