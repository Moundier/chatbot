package com.example.demo.redis;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.stereotype.Component;

import jakarta.annotation.PostConstruct;
import redis.clients.jedis.Jedis;
import redis.clients.jedis.exceptions.JedisConnectionException;

@Component
public class RedisConfig {

    private Jedis jedis;

    public RedisConfig(@Value("${redis.host}") String host, @Value("${redis.port}") int port) {
        this.jedis = new Jedis(host, port);
    }

    @Bean
    public Jedis jedis() {
        return jedis;
    }

    @PostConstruct
    public void pingConnection() {

        try {
            jedis.ping();
            System.out.println(RedisStatus.SUCCESS.getMessage());
        } catch (JedisConnectionException e) {
            System.err.println(RedisStatus.ERROR.getErrorMessage(jedis.getClient().getHost(), String.valueOf(jedis.getClient().getPort())));
        }
    }

}
