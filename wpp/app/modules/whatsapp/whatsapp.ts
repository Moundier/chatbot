import { create, Message, Whatsapp } from '@wppconnect-team/wppconnect';
import { QRCode } from '../../models/qrcode/qrcode.model';
import qrService from '../../models/qrcode/qrcode.service';

type MessageFilter = {
    id: string;
    content: string;
    pushname: string;
    shortname: string;
}

export async function wppConnect(): Promise<Whatsapp> {
    
    const connection: Whatsapp = await create({
        session: '',
        logQR: true,
        debug: false,
        disableWelcome: true,
        catchQR: (base64Qr: string, asciiQR: string) => {
            let qrCode: QRCode | null = qrService.parseQRCode(base64Qr);

            if (qrCode) {
                qrService.saveQRCodeImage(qrCode, 'qr-code')
            }
        },
    });

    return connection;
}

export async function onMessage(message: Message): Promise<void> {
    
    const filtered: Partial<MessageFilter> = {
        id: message.id,
        content: message.content,
        pushname: message.sender.pushname,
        shortname: message.sender.shortName,
    };

    console.log('[Message]:\n' + JSON.stringify(filtered, null, 1));
}