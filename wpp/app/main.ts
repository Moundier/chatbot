import botRepository from './models/bot/bot.repository';
import messageService from './models/message/message.service';

import { Channel, ConsumeMessage } from 'amqplib';

import { wppConnect } from './modules/whatsapp/whatsapp';
import { Message, Whatsapp } from '@wppconnect-team/wppconnect';

import { getChannel } from './modules/rabbitmq/rabbitmq';
import { QUEUE_NAMES } from './modules/rabbitmq/rabbitmq.config';

export const main: (() => Promise<void>) = (async (): Promise<void> => {
    
    const channel: Channel = await getChannel();
    const client: Whatsapp = await wppConnect();

    client.onAnyMessage((message: Message) => {
        let response: string | null = botRepository.getCommandResponse(message.content);

        if (response) {
            client.sendText(message.from, response);
        }

        if (messageService.isDisposable(message)) {
            return;
        } 

        let fragment: MessageFragmented | null = messageService.getMessageFragmented(message);

        if (message.from) {
            console.log(`${JSON.stringify(fragment)}\n`);
        }

        channel.sendToQueue(QUEUE_NAMES.requestQueue, Buffer.from(JSON.stringify(fragment)), {
            persistent: true,
        });

    });

    channel.consume(QUEUE_NAMES.responseQueue, async (consumeMessage: ConsumeMessage | null) => {
        if (!consumeMessage) {
            return;
        }

        console.log(consumeMessage)

        const message: Message = JSON.parse(consumeMessage.content.toString());
        console.log('Message received from RabbitMQ:', message);

        await client.sendText(message.from, `Received your message: ${message.content}`);
        channel.ack(consumeMessage);
    }, { noAck: false });

});
