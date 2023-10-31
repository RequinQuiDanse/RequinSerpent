from bot import bot
import csv
import asyncio

async def get_messages_from_channel(channel_id, write=False, file=None):
    channel =  bot.get_channel(channel_id)
    print(channel)
    messages = []
    async for msgs in channel.history(limit=100, oldest_first = True):
        try:
            messages.append((msgs.author.name, msgs.content))
        except:
            pass

    if write:
        with open(file, mode='a', newline='') as fichier:
            writer = csv.writer(fichier, delimiter=",")
            for msg in messages:
                if "http" not in msg[1]:
                    writer.writerow([msg[0],'"'+msg[1].replace("\n","")+'"'])
        fichier.close()

    return messages

print(asyncio.run(get_messages_from_channel(channel_id=781952289430306846)))