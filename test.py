import unittest
import asyncio
import motor.motor_asyncio

import city_generator

client = motor.motor_asyncio.AsyncIOMotorClient('localhost', 27017)
db = client.local
loop = asyncio.get_event_loop()

async def get_all_cities(cap=500) -> list:
    return await db.Cities.find({}).to_list(cap)

async def get_city_by_index(index) -> list:
    return await db.Cities.find_one({'index': {'$eq': index}})

class TestCity(unittest.TestCase):

    def test_collection_cleaning(self):
        loop.run_until_complete(city_generator.remove_cities())

    def test_insert_city(self):
        loop.run_until_complete(city_generator.remove_cities())
        loop.run_until_complete(city_generator.insert_city(1))
        self.assertEqual(len(loop.run_until_complete(get_all_cities(200))), 1)
        loop.run_until_complete(city_generator.remove_cities())

    def test_get_city(self):
        loop.run_until_complete(city_generator.remove_cities())
        loop.run_until_complete(city_generator.insert_city(5))
        self.assertIn('name', loop.run_until_complete(get_city_by_index(5)))
        self.assertIn('index', loop.run_until_complete(get_city_by_index(5)))
        self.assertIn('roads', loop.run_until_complete(get_city_by_index(5)))
        loop.run_until_complete(city_generator.remove_cities())

    def test_get_replace_city(self):
        loop.run_until_complete(city_generator.remove_cities())
        loop.run_until_complete(city_generator.insert_city(5))
        city = loop.run_until_complete(city_generator.get_city(5))
        city['name'] = 'replaced_city'
        loop.run_until_complete(city_generator.replace_city(5, city))
        loop.run_until_complete(city_generator.remove_cities())

    def test_state_generation(self):
        loop.run_until_complete(city_generator.remove_cities())
        loop.run_until_complete(city_generator.generate_state(20, 60))
        self.assertEqual(len(loop.run_until_complete(get_all_cities(200))), 20)
        loop.run_until_complete(city_generator.remove_cities())

if __name__ == '__main__':
    unittest.main()