package com.example.demo.redis;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.stereotype.Component;
import redis.clients.jedis.Jedis;

@Component
public class RedisConfig {

    @Bean
    public Jedis jedis(@Value("${redis.host}") String host, @Value("${redis.port}") int port) {
        return new Jedis(host, port);
    }
}