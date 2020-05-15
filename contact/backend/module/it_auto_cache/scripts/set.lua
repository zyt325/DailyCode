---
--- Created by yanghg.
--- DateTime: 17-12-27 下午3:58
---

redis.call('SET', unpack(ARGV))


return redis.call('SET', unpack(KEYS))
