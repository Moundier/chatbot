
cd ../../app;

python -m venv venv; 
source venv/bin/activate;

pip install -qU langchain 
pip install -qU langchain_community
pip install -qU langchain-ollama
pip install -qU tiktoken
pip install -qU bs4
pip install -qU chromadb # >>> https://docs.trychroma.com/

# >>> Installs ollama to /usr/local
curl -fsSL https://ollama.com/install.sh | sh

ollama pull nomic-embed-text;
ollama pull mistral
