import { create, Message, Whatsapp } from '@wppconnect-team/wppconnect';
import { QRCode } from '../../models/qrcode/qrcode.model';
import qrService from '../../models/qrcode/qrcode.service';

type MessageFilter = {
    id: string,
    content: string,
    from: string,
    to: string,
    timestamp: number,
}

export async function wppConnect(): Promise<Whatsapp> {
    
    const connection: Whatsapp = await create({
        session: '',
        folderNameToken: 'tokens',
        logQR: true,
        debug: false,
        disableWelcome: true,
        catchQR: (base64Qr: string, asciiQR: string) => {
            let qrCode: QRCode | null = qrService.parseQRCode(base64Qr);

            if (qrCode) {
                qrService.saveQRCodeImage(qrCode, 'qr-code')
            }
        },
        updatesLog: false,
    });

    return connection;
}

export async function onAnyMessageEvent(message: Message): Promise<void> {

    let messageEnqueued: Partial<MessageFilter> = {
        id: message.id,
        content: message.content,
        from: message.from,
        to: message.to,
        timestamp: message.timestamp,
    }

    console.log(messageEnqueued);
}