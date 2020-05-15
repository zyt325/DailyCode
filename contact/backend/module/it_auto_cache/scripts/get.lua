---
--- Created by yanghg.
--- DateTime: 17-12-12 下午3:28
---

--- Try to get value by the given key
local value = redis.call('GET', KEYS[1])
if (value)
then
    --- If the key exists, hits += 1
    redis.call('INCRBY', KEYS[2], 1)
else
    --- If the key doesn't exist, misses += 1
    redis.call('INCRBY', KEYS[3], 1)
end
--- Return the value
return value
