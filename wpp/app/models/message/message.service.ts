import { Message } from "@wppconnect-team/wppconnect";

export class MessageFragmentedService {
    
    public getMessageFragmented(message: Message): MessageFragmented | null {

        if (message === null) return null;

        const messageFragmented: MessageFragmented = {
            id: message.id,
            content: message.content,
            from: message.from,
            to: message.to,
            timestamp: message.timestamp,
            phoneNumber: message.from.split('@')[0],
            possibleNames: {
                name: message.sender.name,
                shortName: message.sender.shortName,
                pushname: message.sender.pushname,
            }
        };

        return messageFragmented;
    }

    public isDisposable(message: Message): boolean {
        switch (true) {
            case message.fromMe:
                console.log('[Ignoring] - Message from myself');
                return true;
            case message.isGroupMsg:
                console.log('[Ignoring] - Group message');
                return true;
            case message.isNotification:
                console.log('[Ignoring] - Notification message');
                return true;
            case message.type === 'image':
                console.log('[Ignoring] - Image message');
                return true;
            case message.type === 'video':
                console.log('[Ignoring] - Video message');
                return true;
            case message.mediaData.type === 'unknown':
                console.log('[Ignoring] - Unknown media type');
                return true;
            default:
                return false;
        }
    }
}

export default new MessageFragmentedService();