import { getChannel } from './modules/rabbitmq/rabbitmq';
import { wppConnect, onMessage } from './modules/whatsapp/whatsapp';
import botRepository from './models/bot/bot.repository';
import { Channel, ConsumeMessage } from 'amqplib';
import { Message, Whatsapp } from '@wppconnect-team/wppconnect';

export const main: (() => Promise<void>) = (async (): Promise<void> => {
    
    config();
    const channel: Channel = await getChannel();
    const client: Whatsapp = await wppConnect();

    client.onAnyMessage((message: Message) => {
        let response: string | null = botRepository.getCommandResponse(message.content);

        if (response) {
            client.sendText(message.from, response);
        }

        if (message.fromMe) {
            console.log(`${message.content}`);
            return;
        }

        channel.sendToQueue('synchronizer_queue', Buffer.from(JSON.stringify(message)), {
            persistent: true,
        });

        onMessage(message);
    });

    channel.consume('response_rag_queue', async (consumeMessage: ConsumeMessage | null) => {
        if (!consumeMessage) {
            return;
        }

        const message = JSON.parse(consumeMessage.content.toString());
        console.log('Message received from RabbitMQ:', message);

        await client.sendText(message.from, `Received your message: ${message.content}`);
        channel.ack(consumeMessage);
    }, { noAck: false });

});

const config: (() => Promise<void>) = (async (): Promise<void> => {
    
    let services: object[] = [
        {
            name: 'RabbitMQ',
            address: ['http://localhost:15672'],
            environment: { user: 'guest', pass: 'guest' },
            timestamp: new Date().toISOString(),
        },
        {
            name: 'Redis',
            address: ['http://localhost:6379'],
            environment: { password: 'secret' },
            timestamp: new Date().toISOString(),
        },
        {
            name: 'Redis Insight',
            address: ['http://localhost:5540'],
            timestamp: new Date().toISOString(),
        },
        {
            name: 'PgVector',
            address: ['http://localhost:5432'],
            environment: {
                user: 'postgres',
                password: 'postgres',
                db: 'postgres',
            },
            timestamp: new Date().toISOString(),
        },
        {
            name: 'PgAdmin',
            address: ['http://localhost:80'],
            environment: JSON.stringify({email: 'admin@gmail.com', password: '123456'}, null, 1),
            timestamp: new Date().toISOString(),
        },
    ];

    console.table(services);
});