package com.example.demo.scheduler;

import org.springframework.amqp.rabbit.core.RabbitTemplate;
import org.springframework.stereotype.Service;

import com.example.demo.message.Message;
import com.example.demo.redis.RedisService;
import com.example.demo.shared.gson.GsonService;
import com.google.gson.Gson;

import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.Executors;
import java.util.concurrent.ScheduledExecutorService;
import java.util.concurrent.ScheduledFuture;
import java.util.concurrent.TimeUnit;

import lombok.RequiredArgsConstructor;

@Service
@RequiredArgsConstructor
public class SchedulerService {

    private final RabbitTemplate rabbitTemplate;
    private final RedisService redisService;
    private final GsonService gsonService;

    private final ScheduledExecutorService scheduler;
    private ConcurrentHashMap<String, ScheduledFuture<?>> scheduledTasks = new ConcurrentHashMap<>();;

    public void process(Message payload) {
        
        final String key = payload.getPhoneNumber();
        String value = this.gsonService.toJson(payload);

        // Check if the key already exists in Redis
        Message existing = this.gsonService.fromJson(redisService.get(key), Message.class);

        if (existing != null) {
            existing.setMessage(existing.getMessage() + " " + payload.getMessage());
            System.out.println("Update: " + existing.toString());
            value = this.gsonService.toJson(existing);
        } else {
            System.out.println("No existing payload data found. Creating new entry.");
        }

        // Update Redis with the new or updated value
        redisService.update(key, value);

        // Check if a task already exists for this key
        ScheduledFuture<?> sf = scheduledTasks.get(key);
        if (sf != null && !sf.isCancelled()) {
            System.out.println("task-id already exists: " + key + ". Cancelling the old task.");
            sf.cancel(true);  // Use true to interrupt the task if it's running
            scheduledTasks.remove(key); // Remove the old task from the map
        }

        // Create a new task to be scheduled
        Runnable task = () -> {
            System.out.println("task-id executed: " + key + ". Removing from Redis and processing.");
            final String json = redisService.get(key);
            Message data = this.gsonService.fromJson(json, Message.class);
            redisService.delete(key);
            this.publishToQueue(data);
            // sf.cancel(false);
        };

        // Schedule a new task and store the future in the map
        ScheduledFuture<?> newScheduledTask = scheduler.schedule(task, 40, TimeUnit.SECONDS);
        scheduledTasks.put(key, newScheduledTask); // Store the new task in the map

        System.out.println("Scheduled task-id: " + key + " with a 40-second timer.");
    }

    private void publishToQueue(Message payload) {
        // System.out.println("Sending payload to Spark: " + payload.getPhoneNumber() + " - " + payload.getMessage());
        this.rabbitTemplate.convertAndSend(payload);
    }

}
