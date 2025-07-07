#!/bin/bash

# Generate random 12-character alphanumeric password
EMAIL='documentlm@rhobots.ai'
PASSWORD='documentlm'

# Run the curl request silently (no output shown)
curl -s --output /dev/null --request POST \
  --header 'Content-Type: application/json' \
  --data "{
    \"name\": \"DocumentLM\",
    \"email\": \"$EMAIL\",
    \"password\": \"$PASSWORD\"
  }" \
  http://localhost:10000/api/auth/sign-up/email

echo "email: $EMAIL"
echo "password: $PASSWORD"
