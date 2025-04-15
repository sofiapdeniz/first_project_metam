FROM python:3.10   
#define a imagem base, docker hub fornece essa com o python todo instalado
WORKDIR /app
#workdir é o dioretório de trabalho, toda vez que rodar um comando (copy,cmd...) o docker vai estar dentro da pasta /app dentro do container.
COPY subscribe.py .
# copia o script sub da minha máquina p dentro do container, sub.py é o caminho do meu arquivo local(host),'.' representa o dir atual do container, que por conta do WORKDIR é /app, ele pega o sub.py que está no dir consumidor e joga dentro do dir app do container.
RUN pip install paho-mqtt mysql-connector-python
#aqui instala as dependências python dentro do container.
CMD ["python", "subscribe.py"]
#é equivalente a rodar no terminal "python subscribe.py" será executado quanndo o container iniciar.
