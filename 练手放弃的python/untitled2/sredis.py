import redis

pool = redis.ConnectionPool(host='192.168.0.169', decode_responses=True)
r = redis.StrictRedis(connection_pool=pool)



#事务  管道加参数transaction=False
# pipe = r.pipeline()
# pipe.hmset('dict', {'da': 'ds'})
# pipe.hgetall('dict')
# print(pipe.execute())
