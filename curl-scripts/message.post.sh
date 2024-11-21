curl -X POST http://localhost:8080/message \
     -H "Content-Type: application/json" \
     -d '{
           "id": "some-id",
           "content": "E aí, cara.",
           "from": "sender-id",
           "to": "receiver-id",
           "timestamp": 1690137600000,
           "phoneNumber": "1234",
           "possibleNames": {
               "name": "John Doe",
               "shortName": "John",
               "pushname": "JD"
           }
         }'

sleep 1

curl -X POST http://localhost:8080/message \
     -H "Content-Type: application/json" \
     -d '{
           "id": "some-id",
           "content": "Cadê tu?",
           "from": "sender-id",
           "to": "receiver-id",
           "timestamp": 1690137600000,
           "phoneNumber": "1234",
           "possibleNames": {
               "name": "John Doe",
               "shortName": "John",
               "pushname": "JD"
           }
         }'

sleep 1

curl -X POST http://localhost:8080/message \
     -H "Content-Type: application/json" \
     -d '{
           "id": "some-id",
           "content": "E aí, cara.",
           "from": "sender-id",
           "to": "receiver-id",
           "timestamp": 1690137600000,
           "phoneNumber": "12345",
           "possibleNames": {
               "name": "John Doe",
               "shortName": "John",
               "pushname": "JD"
           }
         }'

sleep 1

curl -X POST http://localhost:8080/message \
     -H "Content-Type: application/json" \
     -d '{
           "id": "some-id",
           "content": "Cadê tu?",
           "from": "sender-id",
           "to": "receiver-id",
           "timestamp": 1690137600000,
           "phoneNumber": "12345",
           "possibleNames": {
               "name": "John Doe",
               "shortName": "John",
               "pushname": "JD"
           }
         }'