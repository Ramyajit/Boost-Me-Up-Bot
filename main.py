import discord
import os
import requests
import json
import random
from replit import db
from stay_alive import stay_alive

client = discord.Client()

words = ["sad", "depressed", "unhappy", "angry", "miserable", "depressing","melancholy","gloomy","down","bad"]

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


def update_quotes(quote_message):
  if "qoutes" in db.keys():
    quotes = db["quotes"]
    quotes.append(quote_message)
    db["quotes"] = quotes
  else:
    db["quotes"] = [quote_message]

def delete_quotes(index):
  quotes = db["quotes"]
  if len(quotes) > index:
    del quotes[index]
    db["quotes"] = quotes
  
  

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

  choices = dummy_quotes
  if "quotes" in db.keys():
     choices = choices + list(db["quotes"])

  if any(word in msg for word in words):
    await message.channel.send(random.choice(choices))

  if msg.startswith("$new"):
    quote_message = msg.split("$new ",1)[1]
    update_quotes(quote_message)
    await message.channel.send("New positive quote added.")

  if msg.startswith("$del"):
    quotes = []
    if "quotes" in db.keys():
      index = int(msg.split("$del ",1)[1])
      delete_quotes(index)
      quotes = db["quotes"]
    await message.channel.send(quotes)
    

  



  

stay_alive() 
client.run(os.environ['token'])
