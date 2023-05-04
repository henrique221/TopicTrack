#!/bin/bash

# Criar o ambiente virtual
python3 -m venv venv

# Ativar o ambiente virtual
source venv/bin/activate

# Instalar os pacotes necessários
pip install -r requirements.txt

# Setup
python setup.py install

# Criar as pastas necessárias
mkdir -p data/media

# Executa o projeto
python3 topictrack/summarize.py

# Sair do ambiente virtual
deactivate
