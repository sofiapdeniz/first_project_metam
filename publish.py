import paho.mqtt.client as mqtt  # essa biblioteca faz a minha "ponte" entre o código python e o broker mqtt que no caso é o emqx :)
import time # biblioteca para trabalhar com o tempo em py, pausar a execução do cod, registrar data/hora...

client = mqtt.Client()    # cria o cliente mqtt, instancia um objeto da classe  Client da bib paho-mqtt, vou usar para publicar ou assinar msgs
client.username_pw_set("sofia", "Tatimari13")  # credenciais padrão do emqx, usuário e senha que vou acessar :D
broker_address = "localhost" # aqui indicamos o endereço do broker, nome do container broker
client.connect(broker_address, 1883, 60) # conecta ao broker emqx na porta padrão com um timeout de 60 seg

client.publish("metam/sofia", "Hello Pink World!") #publica no tópico que queremos :) em seguida a msg que queremos enviar
client.publish("metam/sofia", "Olá Mundo Rosa!")

time.sleep(1) # espera um tico antes de encerrar, garantindo q a msg tenha sido enviada de fato
