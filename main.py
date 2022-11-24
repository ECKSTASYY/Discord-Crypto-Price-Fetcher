import discord
import requests
from bs4 import BeautifulSoup
import json
import random

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)


with open('configure.json') as f:
   data = json.load(f)


# Ideally you have this in a .env file but I'm not here to show you that.

NEWS_API_TOKEN = data['News API Token']
DISCORD_BOT_TOKEN = data['Discord Bot Token']




@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return


    if message.content.startswith('$news'):
        try:
            response = requests.get(f"https://newsapi.org/v2/everything?q=crypto&apiKey={NEWS_API_TOKEN}")
            data = json.loads(response.text)
            all_articles = data['articles']

            random_number = random.randint(1,len(all_articles))

            article_author = all_articles[random_number]['source']['name']
            article_title = all_articles[random_number]['title']
            article_Description = all_articles[random_number]['description']
            article_url = all_articles[random_number]['url']
            article_url_embed = all_articles[random_number]['urlToImage']


            embed=discord.Embed(title="", description="", color=0x0080FF)
            embed.set_thumbnail(url=article_url_embed)
            embed.add_field(name="Source:", value=f"{article_author}", inline=False)
            embed.add_field(name="Title:", value=f"{article_title}", inline=False)
            embed.add_field(name="Description:", value=f"{article_Description}", inline=False)
            embed.add_field(name="\nArticle Link:", value=f"[Click Me]({article_url})", inline=False)

            await message.channel.send(embed=embed)


        except:
            return



    if message.content.startswith('$find'):
        coin = message.content.replace('$find ','').lower()

        if coin == 'btc':
            coin = 'bitcoin'

        if coin == 'eth':
            coin = 'Ethereum'
        
        if coin == 'usdt':
            coin = 'Tether'

        if coin == 'usdc':
            coin = 'usd-coin'
        
        if coin == 'doge':
            coin = 'dogecoin'
            
        if coin == 'matic':
            coin = 'Polygon'

        if coin == 'ust':
            coin = 'terrausd'
        
        if coin == 'polkadot':
            coin = 'polkadot-new'
            
        if coin == 'dai':
            coin = 'multi-collateral-dai'

        if coin == 'ltc':
            coin = 'litecoin'

        if coin == 'trx':
            coin = 'tron'
            
        if coin == 'uni':
            coin = 'uniswap'

        if coin == 'shiba':
            coin = 'shiba-inu'

        if coin == 'avax':
            coin = 'Avalanche'

        if coin == 'wbtc':
            coin = 'wrapped-bitcoin'
        

        try:
            url = f'https://coinmarketcap.com/currencies/{coin}'
            page = requests.get(url)
            soup = BeautifulSoup(page.content, 'html.parser')
            crypto_price = soup.find(class_ = 'priceValue').get_text()
            market_cap = soup.find(class_ = 'statsValue').get_text()
            rank = soup.find(class_ = 'namePill namePillPrimary').get_text()

            imageframe = soup.find(class_='sc-aef7b723-0 jPJwrb nameHeader')
            img = imageframe.find_all('img')
            coinImage = img[0]['src']



                
            embed=discord.Embed(title="", description="", color=0x0080FF)
            embed.set_thumbnail(url=coinImage)

            embed.add_field(name="Coin", value=f"{coin.capitalize()}", inline=False)
            embed.add_field(name="Price", value=f"{crypto_price}", inline=False)
            embed.add_field(name="Market Cap", value=f"{market_cap}", inline=False)
            embed.add_field(name="Rank", value=f"{rank}", inline=False)
            embed.add_field(name="Link", value=f"[Click Me]({url})", inline=False)

            await message.channel.send(embed=embed)


        except:
            await message.channel.send(f'Could Not Find {coin.capitalize()}. Try The Full Version Like **Bitcoin**!')



client.run(DISCORD_BOT_TOKEN)

