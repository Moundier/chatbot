package com.example.demo.scheduler;

import org.springframework.stereotype.Service;

import com.example.demo.redis.RedisService;
import com.google.gson.Gson;

import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.Executors;
import java.util.concurrent.ScheduledExecutorService;
import java.util.concurrent.ScheduledFuture;
import lombok.RequiredArgsConstructor;

@Service
@RequiredArgsConstructor
public class SchedulerService {

    private RedisService redisService;
    private ScheduledExecutorService scheduler;
    private ConcurrentHashMap<String, ScheduledFuture<?>> scheduledTasks;

    // public SchedulerService() {
    //     this.scheduler = Executors.newScheduledThreadPool(1);
    //     this.scheduledTasks = new ConcurrentHashMap<>();
    //     // this.gson = new Gson();
    // }

    // public void process(FromNumber payload) {
    //     final String key = payload.getPhoneNumber();
    //     String value = gson.toJson(payload);

    //     // Check if the key already exists in Redis
    //     FromNumber existing = gson.fromJson(redisClient.get(key), FromNumber.class);

    //     if (existing != null) {
    //         existing.setMessage(existing.getMessage() + " " + payload.getMessage());
    //         System.out.println("Update: " + existing.toString());
    //         value = gson.toJson(existing);
    //     } else {
    //         System.out.println("No existing payload data found. Creating new entry.");
    //     }

    //     // Update Redis with the new or updated value
    //     redisClient.update(key, value);

    //     // Check if a task already exists for this key
    //     ScheduledFuture<?> sf = scheduledTasks.get(key);
    //     if (sf != null && !sf.isCancelled()) {
    //         System.out.println("task-id already exists: " + key + ". Cancelling the old task.");
    //         sf.cancel(false);
    //     }

    //     // Create a new task to be scheduled
    //     Runnable task = () -> {
    //         System.out.println("task-id executed: " + key + ". Removing from Redis and processing.");
    //         final String json = redisClient.get(key);
    //         FromNumber data = gson.fromJson(json, FromNumber.class);
    //         redisClient.delete(key);
    //         sendToSpark(data);
    //     };

    //     // Schedule a new task and store the future in the map
    //     ScheduledFuture<?> newScheduledTask = scheduler.schedule(task, 40, TimeUnit.SECONDS);
    //     scheduledTasks.put(key, newScheduledTask); // Store the new task in the map

    //     System.out.println("Scheduled task-id: " + key + " with a 40-second timer.");
    // }

    // private void sendToSpark(FromNumber payload) {
    //     System.out.println("Sending payload to Spark: " + payload.getPhoneNumber() + " - " + payload.getMessage());
    // }

}
