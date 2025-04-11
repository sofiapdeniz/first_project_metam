import paho.mqtt.client as mqtt  # essa biblioteca faz a minha "ponte" entre o código python e o broker mqtt que no caso é o emqx :)
import time # biblioteca para trabalhar com o tempo em py, pausar a execução do cod, registrar data/hora...
import json #adicionando o modulo JSON ne gata vamo testar :D

client = mqtt.Client()    # cria o cliente mqtt, instancia um objeto da classe  Client da bib paho-mqtt, vou usar para publicar ou assinar msgs
client.username_pw_set("sofia", "Tatimari13")  # credenciais padrão do emqx, usuário e senha que vou acessar :D
broker_address = "localhost" # aqui indicamos o endereço do broker.
client.connect(broker_address, 1883, 60) # conecta ao broker emqx na porta padrão com um timeout de 60 seg

mensagem = {   # aqui estou criando um dicionário, simulando dados de um sensor
    "dispositivo": "sensor_1",
    "temperatura": 23.7,
    "umidade": 61,
    "status": "ativo",
    "timestamp": time.time() # trem legal, serve para saber quando a mensagem foi enviada, ele conta todos os segundos que se passaram desde 1 de janeiro de 1970, na mensagem NESSE caso, irá retornar um numero gigantye pois representa os segundos, mas tem como sim transformar isso em uma data :) 
}

mensagem_json = json.dumps(mensagem) #json.dumps é oq transforma o dicionário em um texto no formato JSON, agora o dic "mensagem" se transformou em "mensagem_json"

client.publish("metam/sofia", mensagem_json) # mesmo esquema de antes, cliente.publish para enviar a mensagem, tópico em seguida e depois mandamos o dicionário que foi formatado em json e agora é uma variavel contendo JSON (str) "mensagem_json"

time.sleep(1) # espera um tico antes de encerrar, garantindo q a msg tenha sido enviada de fato
