curl -X POST http://localhost:8080/message \
     -H "Content-Type: application/json" \
     -d '{"phoneNumber": "1234", "message": "Eai cara!"}'

sleep 1

curl -X POST http://localhost:8080/message \
     -H "Content-Type: application/json" \
     -d '{"phoneNumber": "1234", "message": "Cade tu?"}' 

sleep 1

curl -X POST http://localhost:8080/message \
     -H "Content-Type: application/json" \
     -d '{"phoneNumber": "12345", "message": "Eai cara!"}'

sleep 1

curl -X POST http://localhost:8080/message \
     -H "Content-Type: application/json" \
     -d '{"phoneNumber": "12345", "message": "Cade tu?"}' 