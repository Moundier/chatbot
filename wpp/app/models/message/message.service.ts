import { Message } from "@wppconnect-team/wppconnect";
import { MessageFragmented } from "./message.model";

const IGNORED_NUMBERS = [
    '555584510561', // Maran
    '555591737769', // Alencar
    '555591980995', // Friedhein
];

type MessageFilter = {
    text: string; 
    condition: boolean;
}

export class MessageFragmentedService {
    
    public getMessageFragmented(message: Message): MessageFragmented | null {

        if (Object.is(message, null)) {
            return null;
        }

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
    
    public matchesChosen(message: Message): boolean {
        const senderNumber = message.from.split('@')[0];
    
        if (IGNORED_NUMBERS.includes(senderNumber)) {
            return true;
        }
    
        return false;
    }

    public matchesRule(message: Message): boolean {

        const rules: MessageFilter[] = [
            { text: 'INFO [IGNORED] - From sender', condition: message.fromMe },
            { text: 'INFO [IGNORED] - Group message', condition: message.isGroupMsg },
            { text: 'INFO [IGNORED] - System notification', condition: message.isNotification },
            { text: 'INFO [IGNORED] - Image', condition: message.type === 'image' },
            { text: 'INFO [IGNORED] - Video', condition: message.type === 'video' },
            { text: 'FAIL [IGNORED] - Unsupported media type', condition: message.mediaData?.type === 'unknown' },
        ];
    
        const match: MessageFilter | undefined = rules.find(rule => rule.condition);
    
        if (match) {
            const time = new Date().toISOString();
            console.log(`[${time}] ${match.text}`);
            return true;
        }
    
        return false;
    }
    
}

export default new MessageFragmentedService();