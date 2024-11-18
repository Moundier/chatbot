package com.example.demo.message;

import org.apache.tomcat.util.json.JSONParser;
import org.springframework.amqp.rabbit.annotation.RabbitListener;
import org.springframework.amqp.rabbit.core.RabbitTemplate;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;

import com.example.demo.scheduler.SchedulerService;
import com.example.demo.shared.gson.GsonService;
import com.rabbitmq.tools.json.JSONUtil;

import lombok.RequiredArgsConstructor;

@Component
@RequiredArgsConstructor
public class MessageConsumer {

    private final MessageService messageService;

    @Value("${queue.response}")
    private String outputQueue;

    @RabbitListener(queues = "${queue.request}")
    public void consumeMessage(String message) {
        this.messageService.processIncomingFragmentedMessage(message);
    }
    
}
