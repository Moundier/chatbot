package com.example.demo.message;

import org.springframework.amqp.rabbit.core.RabbitTemplate;
import org.springframework.stereotype.Service;

import com.example.demo.scheduler.SchedulerService;
import com.example.demo.shared.gson.GsonService;

import lombok.RequiredArgsConstructor;

@Service
@RequiredArgsConstructor
public class MessageService {
  
    private final SchedulerService schedulerService;
    private final RabbitTemplate rabbitTemplate;
    private final GsonService gsonService;

    public void processIncomingFragmentedMessage(String message) {
        Class<MessageFragment> clazz = MessageFragment.class;
        MessageFragment messageFragment = gsonService.fromJson(message, clazz);
        // schedulerService.process(messageFragment); 
    }
}
