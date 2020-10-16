import redis

pool = redis.ConnectionPool(host='192.168.0.169', decode_responses=True)
r = redis.StrictRedis(connection_pool=pool)

sub = r.pubsub()

sub.subscribe('channel')
while True:
    for item in sub.listen():
        if item['type'] == 'message':
            print(item['channel'], item['data'])
