#!/bin/bash

urls=(
  "http://localhost:80"
  "http://localhost:5540"
  "http://localhost:15672"
  # "http://localhost:5050"
  "http://127.0.0.1/login?next=/"
)

for url in "${urls[@]}"; do
  chromium "$url"
done

# webui
# name admin@gmail.com
# email admin@gmail.com
# password admin@gmail.com

# sudo docker exec -it /bin/bash