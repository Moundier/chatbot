package com.example.demo.rabbit;

import org.springframework.amqp.rabbit.connection.CachingConnectionFactory;
import org.springframework.amqp.rabbit.connection.ConnectionFactory;
import org.springframework.amqp.core.Queue;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

import jakarta.annotation.PostConstruct;

@Configuration
public class RabbitConfig {

    private final String host;
    private final int port;

    public RabbitConfig(
        @Value("${spring.rabbitmq.host}") String host,
        @Value("${spring.rabbitmq.port}") int port
    ) {
        this.host = host;
        this.port = port;
    }

    @Bean
    public Queue queueProcessing() {
        return new Queue("processing_queue");
    }

    @PostConstruct
    public ConnectionFactory connectionFactory() {
        return new CachingConnectionFactory(host, port);
    }

    @PostConstruct
    public void pingConnection() {
        try {
            ConnectionFactory factory = connectionFactory();
            factory.createConnection();
            System.out.println(RabbitStatus.SUCCESS.getMessage());
        } catch (Exception e) {
            System.err.println(RabbitStatus.ERROR.getErrorMessage(this.host, String.valueOf(this.port)));
        }
    }
}
