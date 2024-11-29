#!/bin/bash

urls=(
  "http://localhost:5540"
  "http://localhost:15672"
  "http://localhost:5050"
)

for url in "${urls[@]}"; do
  chromium "$url"
done
