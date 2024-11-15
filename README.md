# Messaging System for WhatsApp

### Overview
- **wpp**: Connects and handles WhatsApp messages.  
- **synchronizer**: Manages message pipeline and synchronization.  
- **rag**: Processes and generates intelligent replies.

### Tech Stack
- **Spring**: Controls message synchronization and routing.  
- **Python**: Powers RAG (retrieval-augmented generation) for responses.  
- **Postgres with PgVector**: Stores vectorized data for quick retrieval.  
- **Redis**: Temporary data caching for speed.
- **RabbitMQ**: Message transport.