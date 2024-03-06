import redis as rd

redis = None

def get_redis():
    global redis
    if not redis:
        redis = rd.Redis()
    return redis

if __name__ == '__main__':
    r = get_redis()
    r.ping()