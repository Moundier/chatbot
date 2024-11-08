import { create, Message, Whatsapp } from '@wppconnect-team/wppconnect';
import { QrCode } from './app/models/qrcode/qrcode.model';

import botCommandsRepository from './app/models/bot/bot.repository';
import qrCodeService from './app/models/qrcode/qrcode.service';

export const main: (() => Promise<void>) = (async (): Promise<void> => {

    let client = await wppConnect();

    client.onAnyMessage((message: Message) => {

        let response: string | null = botCommandsRepository.getCommandResponse(message.content);

        if (response) {
            client.sendText(message.from, response);
        }

        if (message.fromMe) {
            console.log(`${message.content}`);
            return;
        }

        messageContent(message);

    });

});

async function wppConnect(): Promise<Whatsapp> {
    
    const connection: Whatsapp = await create({
        session: '',
        logQR: true,
        debug: false,
        disableWelcome: true,
        catchQR: (base64Qr: string, asciiQR: string) => {

            let qrCode: QrCode | null = qrCodeService.parseQrCode(base64Qr);

            if (qrCode) {
                qrCodeService.saveQrCodeImage(qrCode, 'qr-code')
            }
        },
    });

    return connection;
}

async function messageContent(message: Message): Promise<void> {

    const dto: object = {
        id: message.id, // id do usuario
        content: message.content, // mensagem
        pushname: message.sender.pushname, // Nome q ele exibe
        shortname: message.sender.shortName, // Nome q eu salvei
    }

    console.log('[Message]:\n' + JSON.stringify(dto, null, 1));
}

main().catch((e: unknown) => console.error(e));
