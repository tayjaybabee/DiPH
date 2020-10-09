#!/usr/bin/env python

import os
import pickle
from pathlib import Path
from time import time

import discord
import requests
from dotenv import load_dotenv
from inspyred_print import Color, Format


fmt_end = Format.end_mod
red = Color.red

load_dotenv()
client = discord.Client()
TOKEN = os.getenv("DISCORD_TOKEN")


class HistoryTracker(object):
    def __init__(self):
        app_dir = '~/Inspyre-Softworks/diph'
        app_data_dir = app_dir + '/data'

        cache_dir = app_data_dir + '/cache'
        res_cache_dir = Path(cache_dir).expanduser()

        stat_data_dir = app_data_dir + '/stats'
        res_data_dir = Path(stat_data_dir).expanduser()

        stat_data_filename = 'stats.pickle'
        self.data_filepath = Path(stat_data_dir + '/' + stat_data_filename
                                  ).expanduser()

        self.data = None

        if not res_data_dir.exists():
            os.makedirs(res_data_dir)

        if not res_cache_dir.exists():
            os.makedirs(res_cache_dir)

    def add_entry(self, lookup_res):
        new_entry_title = 'entry' + '_' + str(len(self.data['call_history']))
        new_entry = {
            new_entry_title: {
                'time': time(),
                'usd_value': lookup_res['USD'],


            }
        }
        self.data['call_history'].update(new_entry)


    def load(self):
        if self.data_filepath.exists() and self.data_filepath.is_file():
            with open(self.data_filepath, 'rb') as f:
                stats_data = pickle.load(f)
                print('Loaded previous stats!')
        else:
            stats_data = {
                'created': time(),
                'trending_last': None,
                'call_history': {
                    'sample': {
                        'time': time(),
                        'usd_value': '',
                        'trending': '',
                    }
                }
            }

        self.data = stats_data

        return self.data

    def write(self):
        with open(self.data_filepath, 'wb') as f:
            pickle.dump(self.data, f)


history = HistoryTracker()


def clean_exit(reason):
    print('\nRequesting write of statistics')
    history.write()

    print(f'Exiting! Reason: {reason}')
    exit(0)


# print(dir(client))


@client.event
async def on_ready():
    """Short summary.

    Returns
    -------
    def
        Description of returned object.

    Raises
    -------
    ExceptionName
        Why the exception is raised.

    Examples
    -------
    Examples should be written in doctest format, and
    should illustrate how to use the function/class.
    >>>

    """
    print(f"{red}We have logged in as {client.user}{fmt_end}")
    # print(dir(client))
    print(client.users)


cmd_prefix = "$"
attr_prefix = "."

stats_history = history.load()


def grab_btc_price(traditional_currency):
    url = 'https://blockchain.info/ticker'

    res = requests.get(url)

    data = res.json()

    print(data)

    price = data[traditional_currency]['15m']

    sym = data[traditional_currency]['symbol']

    f_price = "{:,.2f}".format(price)

    f_price = sym + str(f_price)

    history.add_entry(data)

    return f_price, price


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    sender = message.author
    content = message.content

    # First, let's check to see if our received message is a request to change an attribute
    if content.startswith(attr_prefix):
        content == content.split(" ").pop()

    if content.startswith("$hello"):
        await message.channel.send("Hello!")
        await message.channel.send(f"{dir(message)}")
        await message.tts(message)

    elif content.startswith(f"{cmd_prefix}weather"):
        print(f"Received request from {sender} to fetch weather")
        await message.channel.send("Here I would deliver the weather.")
        print("Responded")

    elif content.lower().startswith(f'{cmd_prefix}btc'):
        currency = 'USD'
        cmd_list = content.split(' ')
        if len(cmd_list) >= 2:
            currency = cmd_list[1]

        btc_price = grab_btc_price(currency)

        btc_price_raw = btc_price[1]

        trending_direction = None

        print(dir(history))

        last = history.data['call_history'][list(history.data['call_history'].keys())[-2]]['usd_value']['15m']
        print(last)
        if last == btc_price_raw:
            treanding_direction = None

        elif last >= btc_price_raw:
            trending_direction = 'down'

        elif last <= btc_price_raw:
            trending_direction = 'up'

        btc_price = btc_price[0]

        statement = f"The price of one Bitcoin in {currency} is: {btc_price} ({trending_direction})"

        await message.channel.send(statement)


    else:
        msg_statement = f"{sender} sent a message to {message.channel}:\n{content}"
        if not content == "":
            print(msg_statement)
    print("")


@client.event
async def on_member_join(member):
    print(f"{member.name} joined at {member.joined_at}")
    print(dir(member))


class Bot:
    def __init__(self):

        self.client = client
        self.client_run = self.client.run(TOKEN)


bot = Bot()

clean_exit('User exit')
