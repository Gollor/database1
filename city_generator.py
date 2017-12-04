import motor.motor_asyncio
import numpy as np
import asyncio

syllable_first  = ["Ki", "Lv", "Khar", "Odes", "Dni", "Myko", "Vin",    "Uzh",   "Zapo",   "Lu",  "Cher",  "Kher"]
syllable_second = ["ev", "iv", "kiv" , "sa",   "pro", "laiv", "nytsia", "horod", "rizhia", "tsk", "nihiv", "son"]

client = motor.motor_asyncio.AsyncIOMotorClient('localhost', 27017)
db = client.local

async def insert_city(index):
    name = np.random.choice(syllable_first) + np.random.choice(syllable_second)
    document = {"index": index, "name": name, "roads": []}
    result = await db.Cities.insert_one(document)

async def get_city(index):
    document = await db.Cities.find_one({'index': {'$eq': index}})
    return document

async def replace_city(index, obj):
    document = await db.Cities.replace_one({'index': {'$eq': index}}, obj)

async def insert_road(index, cities_amount):
    cityA = np.random.randint(cities_amount)
    while True: # do..while loop emulation
        cityB = np.random.randint(cities_amount)
        if cityB != cityA:
            break
    cityAobj = await get_city(cityA)
    cityBobj = await get_city(cityB)
    cityAobj["roads"].append({"index": cityB, "name": cityBobj["name"]})
    cityBobj["roads"].append({"index": cityA, "name": cityAobj["name"]})
    await replace_city(cityA, cityAobj)
    await replace_city(cityB, cityBobj)

async def remove_cities():
    await db.Cities.delete_many({})

async def generate_state(cities_amount, roads_amount):
    await remove_cities()
    for i in range(cities_amount):
        await insert_city(i)
    for i in range(roads_amount):
        await insert_road(i, cities_amount)

loop = asyncio.get_event_loop()
loop.run_until_complete(generate_state(40, 120))
