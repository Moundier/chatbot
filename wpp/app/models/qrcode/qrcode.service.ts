import { QrCode } from "./qrcode.model";
import { promises as fs } from 'fs';

export class QrCodeService {
    
    public parseQrCode(base64Qr: string): QrCode | null {
        let matches = base64Qr.match(/^data:([A-Za-z-+/]+);base64,(.+)$/);
        
        if (matches) {
            return {
                type: matches[1],
                data: Buffer.from(matches[2], 'base64'),
            };
        }
        
        return null;
    }

    public async saveQrCodeImage(qrCode: QrCode, name: string): Promise<void> {
        if (qrCode.data) {
            const f: string = name.endsWith('.png') ? name : `${name}.png`;
            await fs.writeFile(f, qrCode.data, 'binary');
            return;
        }

        console.error('Error: No QR code data.');
        return;
    }
}

export default new QrCodeService();