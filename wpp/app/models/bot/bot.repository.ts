import { Message } from "@wppconnect-team/wppconnect";
import commands from "./bot.cmds";

export class BotCommandsRepository {
    
    public hasCommand(command: string): boolean {
        return commands.has(command);
    }

    public getCommandResponse(command: string): string | null {
        return commands.get(command) ?? null;
    }
}

export default new BotCommandsRepository();