# !/bin/bash

# Set your gitlab credentials
GIT_USERNAME="garamoundier"
GIT_TOKEN="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"  # PAT
GITHUB="https://$GIT_USERNAME:$GIT_TOKEN@github.com/Moundier"

CB="$GITHUB/chatbot.git"

git clone $CB
sudo chown -R "$OWNER":"$OWNER" ./
