# bot.py
import os
import json

from discord.ext import commands
from dotenv import load_dotenv
from decimal import *
from collections import defaultdict

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
ALL = 'all'
# TODO: Move emoji list to external file
emojis = [
    '\N{Regional Indicator Symbol Letter A}',
    '\N{Regional Indicator Symbol Letter B}',
    '\N{Regional Indicator Symbol Letter C}',
    '\N{Regional Indicator Symbol Letter D}',
    '\N{Regional Indicator Symbol Letter E}',
    '\N{Regional Indicator Symbol Letter F}',
    '\N{Regional Indicator Symbol Letter G}',
    '\N{Regional Indicator Symbol Letter H}',
    '\N{Hamburger}',
]
bot = commands.Bot(command_prefix='!')

# TODO: Add some argument validations, file validations, and null checks
@bot.command(name='bill', help='Format must be item1-price1 item2-price2 ... : person1 person2...')
async def setBill(ctx, *argument):
    if (not argument):
        await ctx.send('Please use !help for an example of how to use !bill')
        return

    data = {}
    items=argument[:argument.index(':')]
    people=list(argument[argument.index(':') + 1:])
    if len(items) < 1 or len(people) < 1:
        await ctx.send('Please use !help for an example of how to use !bill')
        return
    elif (len(people) > len(emojis) - 1): 
        await ctx.send(f'Only accepts max of {(len(emojis) - 1)} unique persons')
        return

    peopleDict = {}
    peopleFomattedString = ''
    for i in range(len(people)):
        peopleDict[emojis[i]] = people[i]
        peopleFomattedString += f'{emojis[i]} -  {people[i]}\n'
    peopleFomattedString += f'{emojis[len(emojis)-1]} - {ALL}'
    data['people'] = peopleDict
    await ctx.send('Legend (Emoji - Person)')
    await ctx.send(peopleFomattedString)

    itemsDict = {}
    for item in items:
        key,value = item.split('-')
        itemsDict[key] = value
    data['items'] = itemsDict

    messageIds = []
    for item in itemsDict.keys():
        message = await ctx.send(item)
        messageIds.append(message.id)
        for i in range(len(people)):
            await message.add_reaction(emojis[i])
        await message.add_reaction(emojis[len(emojis) - 1])
    data['messageIds'] = messageIds

    with open('data.json', 'w') as outfile:
        json.dump(data, outfile, indent=4)

# TODO: Add some argument validations, file validations, and null checks
@bot.command(name='split', help='Used after bill is inputted and items are properly reacted')
async def splitBill(ctx):
    with open('./data.json') as f:
        data = json.load(f)

    totals = defaultdict(lambda: {'total': Decimal(0), 'items': []})
    itemsNotSplit = []
    for i in range(len(data['messageIds'])):
        message = await ctx.fetch_message(data['messageIds'][i])
        peopleWhoShared = []
        # print(message.reactions)
        counter = 0
        for j in range(len(message.reactions)-1):
            currentEmoji = message.reactions[j]
            if currentEmoji.count > 1:
                peopleWhoShared.append(currentEmoji.emoji)
                counter += 1

        if (message.reactions[len(message.reactions)-1].count > 1):
            cost = Decimal(data['items'][message.content])/(len(message.reactions)-1)
            for ppl in data['people'].keys():
                totals[ppl]['total'] += cost
                totals[ppl]['items'].append(message.content)
        elif (counter > 0):
            cost = Decimal(data['items'][message.content])/counter
            for ppl in peopleWhoShared:
                totals[ppl]['total'] += cost
                totals[ppl]['items'].append(message.content)
        else:
            cost = 0
            itemsNotSplit.append(message.content)

        # print(cost)
    #     print(peopleWhoShared)
    # print(itemsNotSplit)
    # print(totals)

    totalsFormattedString = ''
    for k,v in totals.items():
        totalsFormattedString += data['people'][k] + ' - ' + k
        totalsFormattedString += '\n Ordered: {items}\n Total: ${total}'.format_map(v)
        taxedTotal = round(v['total'] * Decimal('1.13'), 2)
        totalsFormattedString += f', With tax: ${taxedTotal}\n'
    await ctx.send(totalsFormattedString)
    
    if itemsNotSplit:
        await ctx.send(f'Following items not distributed: {itemsNotSplit}')

bot.run(TOKEN)