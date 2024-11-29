import botRepository from './models/bot/bot.repository';
import messageService from './models/message/message.service';

import { Channel, ConsumeMessage } from 'amqplib';

import { wppConnect } from './modules/whatsapp/whatsapp';
import { Message, Whatsapp } from '@wppconnect-team/wppconnect';

import { getChannel } from './modules/rabbitmq/rabbitmq';
import { QUEUE_NAMES } from './modules/rabbitmq/rabbitmq.config';

import { MessageFragmented } from './models/message/message.model';

export const main: (() => Promise<void>) = (async (): Promise<void> => {
    
    const channel: Channel = await getChannel();
    const client: Whatsapp = await wppConnect();

    client.onAnyMessage((message: Message) => {
        let response: string | null = botRepository.getCommandResponse(message.content);

        if (response) {
            client.sendText(message.from, response);
            return;
        }

        if (messageService.matchesChosen(message)) {
            return;
        } 

        if (messageService.matchesRule(message)) {
            return;
        }

        // client.sendText(message.from, `Pong. ${new Date().toISOString()}`);

        let fragment: MessageFragmented | null = messageService.getMessageFragmented(message);

        channel.sendToQueue(QUEUE_NAMES.requestQueue, Buffer.from(JSON.stringify(fragment)), {
            persistent: true,
        });

    });

    channel.consume(QUEUE_NAMES.responseQueue, async (consumeMessage: ConsumeMessage | null) => {
        if (!consumeMessage) {
            return;
        }

        const message: MessageFragmented = JSON.parse(consumeMessage.content.toString());

        await client.sendText(message.from, `Resposta: ${JSON.stringify(message.response)}`);

        channel.ack(consumeMessage);
    }, { noAck: false });

});
