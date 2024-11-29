import sys
import asyncio

from rabbit.rabbit_consume import consume_messages

if __name__ == "__main__":
    try:
        asyncio.run(consume_messages())
    except KeyboardInterrupt:
        system_exit: str = '\n\nShutting down...\n\n' 
        sys.stdout.write(system_exit)
        sys.exit(0)

