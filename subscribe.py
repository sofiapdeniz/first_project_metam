import paho.mqtt.client as mqtt
import json

# precisamos fazer uma função que será chamada quando a conexão com o broker for estabelecida, o paho chama automaticamente quando o client conecta ao broker
def on_connect(client, userdata, flags, rc): #userdata e flags são parâmetros que não estaremos utilizando agora, portanto, o paho espera a assinatura correta, que são esses 4 argumentos, o python aceita tirar mas a biblioteca espera ter esses 4, pra não dar erro deixamos :) lembrando que existem maneiras de esconder, mas vamos deixar assim quietin
    print("Conectado com código de retorno:", rc) #rc significa "return code", indica se a conexão foi bem sucedida, deve retornar 0, se retornar outro valor está errado.
    client.subscribe("metam/sofia") #aqui se inscrevemos no tópico, o cliente vai ouvir mensagens desse tópico.

# def on_message e def on_connect são callbacks da biblioteca paho, padrão mesmo, essa serve para cada vez que uma mensagem chega no tópico que estamos, é chamada.
def on_message(client, userdata, msg):
    print("Mensagem recebida no tópico:", msg.topic) 
    print("Conteúdo da Mensagem (raw):", msg.payload.decode())

    try:
        dados = json.loads(msg.payload.decode())
        print("JSON decodificado:", dados)
    except json.JSONDecodeError:
        print("Não foi possível decodificar a mensagem como JSON.")

client = mqtt.Client()
client.username_pw_set("sofia", "Tatimari13")

client.on_connect = on_connect
client.on_message = on_message
client.connect("localhost", 1883, 60)

client.loop_forever()
