from proxypool.log import logger
from proxypool.db import RedisClient

redis = RedisClient()


def image_pipeline(item):
    logger.info(f"image_pipeline ...")
    return item


def mongo_pipeline(item):
    logger.info(f"mongo_pipeline ...")
    return item


def mysql_pipeline(item):
    logger.info(f"mysql_pipeline ...")
    return item


def redis_pipeline(item):
    logger.info("redis_pipeline ...")
    if item:
        redis.add(item)
    return item


ITEM_PIPELINES = {
    image_pipeline: 300,
    mongo_pipeline: 301,
    mysql_pipeline: 302,
    redis_pipeline: 303
}


