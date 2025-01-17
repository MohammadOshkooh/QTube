import json
import random
from decouple import config
from redis import Redis

redis_connection = Redis(host=config('REDIS_HOST'), port=config('REDIS_PORT'), decode_responses=True)

def generate_random_token() -> str:
    try:
        token = random.randint(10000, 99999)
        if len(str(token)) != 5:
            generate_random_token()
        return str(token)
    except Exception as e:
        return f"error: {str(e)}"



def add_dict_to_redis(key: str, value: [dict, list], *args, **kwargs) -> bool:
    try:
        return redis_connection.set(key, json.dumps(value), **kwargs)
    except:
        return False


def get_dict_from_redis(key: str) -> dict:
    try:
        return {'status': True, "data": json.loads(redis_connection.get(key))}
    except:
        return {'status': False, "data": None}


def delete_item_from_redis(key: str) -> bool:
    try:
        return bool(redis_connection.delete(key))
    except:
        return False

