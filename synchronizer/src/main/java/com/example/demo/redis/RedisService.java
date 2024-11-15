package com.example.demo.redis;

import redis.clients.jedis.Jedis;
import org.springframework.stereotype.Service;

import lombok.RequiredArgsConstructor;

@Service
@RequiredArgsConstructor
public class RedisService {

    private final Jedis jedis;

    public boolean isPresent(String key) {
        return this.get(key) != null;
    }

    public void update(String key, String value) {
        this.jedis.set(key, value);
    }

    public String get(String key) {
        return this.jedis.get(key);
    }

    public void delete(String key) {
        this.jedis.del(key);
    }
}