package com.example.demo.amqp;

import org.springframework.amqp.rabbit.core.RabbitTemplate;
import org.springframework.stereotype.Service;

import lombok.RequiredArgsConstructor;

@Service
@RequiredArgsConstructor
public class QueueService {

	private final RabbitTemplate rabbitTemplate;

	private String INCOMING_QUEUE;
	private String OUTCOMING_QUEUE;

	private void queuePub(String queue, String message) {
		this.rabbitTemplate.convertAndSend(queue, message);
	}
	
	// public void publishTransferencia(Objeto objeto) {
	// 	this.queuePub(INCOMING_QUEUE, JacksonUtil.toString(transferencia));
	// }

	private String queueSub(String queue) {
		return (String) this.rabbitTemplate.receiveAndConvert(queue);
	}

}
