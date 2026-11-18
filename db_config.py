import redis
import yaml
from pymongo import MongoClient

def load_config():
    """Load configuration from the YAML file.

    Returns:
        dict: Configuration data.
    """
    with open("config.yaml", "r") as file:
        return yaml.safe_load(file)

config = load_config()

def get_redis_connection():
    """Create a Redis connection using the configuration.

    Returns:
        Redis: Redis connection object.
    """
    return redis.Redis(
        host=config["redis"]["host"],
        port=config["redis"]["port"],
        db=0,
        # decode_responses=True,
        username=config["redis"]["user"],
        password=config["redis"]["password"],
    )

def get_mongo_connection():
    """Create a Mongo connection using the configuration.
    
        Returns:
            Mongo: MongoDB connection object
        """
    return MongoClient(config["mongo"]["connection_string"])
