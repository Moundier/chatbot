import amqp, { Connection, Channel } from 'amqplib';

export const mqConnect: (() => Promise<Connection>) = (async (): Promise<Connection> => {
    
    try {
        return await amqp.connect('amqp://localhost');
    } catch (error: AggregateError | unknown) {
        const err: string = 'Rabbitmq not running';
        throw new Error(err);
    }
});

export const getChannel: (() => Promise<Channel>) = (async (): Promise<Channel> => {
    
    try {
        
        let connection: Connection = await mqConnect();

        const channel: Channel = await connection.createChannel();
        await channel.assertQueue('request_queue', { durable: true });
        await channel.assertQueue('response_queue', { durable: true });

        return channel;

    } catch (error: unknown) {
        const err: string = 'Depends on Rabbitmq';
        throw new Error(err);
    }
});