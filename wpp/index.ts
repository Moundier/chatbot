import { amqp } from 'amqp';
import { create, Message, Whatsapp } from '@wppconnect-team/wppconnect';
import { promises as fs } from 'fs';

import cmds from './app/modules/bot.cmds';

export interface QrCode {
    type?: string;
    data?: Buffer;
}

export const main: (() => Promise<void>) = (async (): Promise<void> => {

    let client = await wppConnect();

    client.onAnyMessage((message: Message) => {

        if (cmds.has(message.content)) {
            const sender: string = message.from; 
            const respond: string | undefined = cmds.get(message.content)!;
            client.sendText(sender, respond);
            return;
        }

        if (message.fromMe) {
            console.log(`${message.content}`);
            return;
        }

        console.log({
            senderShort: message.sender.shortName, // Nome q eu salvei
            pushname: message.sender.pushname, // Nome q ele exive
            content: message.content, // mensagem
            id: message.id, // id do usuario
        })

    });

});

async function wppConnect(): Promise<Whatsapp> {
    return await create({
        session: '',
        logQR: true,
        debug: false,
        disableWelcome: true,
        catchQR: (base64Qr: string, asciiQR: string) => {
            const matches = base64Qr.match(/^data:([A-Za-z-+\/]+);base64,(.+)$/);
            const qrCodeObject: QrCode = {};

            if (matches === null) return;

            qrCodeObject.type = matches[1];
            qrCodeObject.data = Buffer.from(matches[2], 'base64');

            qrCodeImage(qrCodeObject, "qr-code");
        },
    });
}


export async function qrCodeImage(response: QrCode, name: string): Promise<void> {
    
    if (!response.data) {
        console.warn('No data available to save.');
        return;
    }

    try {
        const filename = name.endsWith('.png') ? name : `${name}.png`;
        await fs.writeFile(filename, response.data, 'binary');
        console.log(`Image ${filename}`);
    } catch (error: unknown) {
        console.error('Error:', error);
    }
}

main();
