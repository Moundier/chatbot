import sys
import asyncio

from rabbit.rabbit_consume import consume_messages

if __name__ == ("__main__"):
    try:
        asyncio.run(consume_messages())
    except KeyboardInterrupt:
        print("\nShutting down gracefully...\n")
        sys.exit(0)

