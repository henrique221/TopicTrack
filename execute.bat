@echo off

REM Criar o ambiente virtual
python -m venv venv

REM Ativar o ambiente virtual
call venv\Scripts\activate

REM Instalar os pacotes necessários
pip install -r requirements.txt

REM Setup
python setup.py install

REM Criar as pastas necessárias
if not exist "data" mkdir data
if not exist "data\media" mkdir data\media

REM Executar o projeto
python topictrack\summarize.py

REM Sair do ambiente virtual
call deactivate
