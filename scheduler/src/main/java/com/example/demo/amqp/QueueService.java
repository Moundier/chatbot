package com.example.demo.amqp;

import java.util.Objects;

import org.springframework.amqp.rabbit.core.RabbitTemplate;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

import lombok.RequiredArgsConstructor;

@Service
@RequiredArgsConstructor
public class QueueService {

    private final RabbitTemplate rabbitTemplate;

    // Uncomment and use these if you need to specify the queue names from properties
    // @Value("${rabbitmq.incoming.queue}")
    // private String incomingQueue;

    // @Value("${rabbitmq.outgoing.queue}")
    // private String outgoingQueue;

    private void enqueue(String queue, String message) {
        this.rabbitTemplate.convertAndSend(queue, message);
    }

    public String getFromQueue(String queueName) {
        Object object = this.rabbitTemplate.receiveAndConvert(queueName);
        
        if (Objects.isNull(object)) return null;

        return object.toString();
    }
}
