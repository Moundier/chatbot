package com.example.demo.message;

import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.example.demo.scheduler.SchedulerService;

import lombok.RequiredArgsConstructor;

@RestController
@RequestMapping("/message")
@RequiredArgsConstructor
public class MessageController {

    private final SchedulerService schedulerService;
  
    @PostMapping
    public ResponseEntity<Message> receiveMessage(@RequestBody Message message) {
        // System.out.println("Received message: " + message);
        this.schedulerService.process(message);
        return new ResponseEntity<>(message, HttpStatus.OK);
    }
}
