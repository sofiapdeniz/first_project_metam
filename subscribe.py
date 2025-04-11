import paho.mqtt.client as mqtt
import json

# precisamos fazer uma função que será chamada quando a conexão com o broker for estabelecida, o paho chama automaticamente quando o client conecta ao broker
def on_connect(client, userdata, flags, rc): #userdata e flags são parâmetros que não estaremos utilizando agora, portanto, o paho espera a assinatura correta, que são esses 4 argumentos, o python aceita tirar mas a biblioteca espera ter esses 4, pra não dar erro deixamos :) lembrando que existem maneiras de esconder, mas vamos deixar assim quietin
    print("Conectado com código de retorno:", rc) #rc significa "return code", indica se a conexão foi bem sucedida, deve retornar 0, se retornar outro valor está errado.
    client.subscribe("metam/sofia") #aqui se inscrevemos no tópico, o cliente vai ouvir mensagens desse tópico.

# def on_message e def on_connect são callbacks da biblioteca paho, padrão mesmo, essa serve para cada vez que uma mensagem chega no tópico que estamos, é chamada.
def on_message(client, userdata, msg):
    print("Mensagem recebida no tópico:", msg.topic) # exibe o nome do tópico que recebeu a mensagem
    print("Conteúdo da Mensagem (raw):", msg.payload.decode()) # "msg.payloadé o conteúdo da msg mas em bytes, decode transforma de bytes para str(utf-8), então a mensagem vai chegar crua.

    try: # TENTA interpretar a string da msg como JSON e transformar em um dicionário python (linha abaixo)
        dados = json.loads(msg.payload.decode())
        print("JSON decodificado:", dados) # se rolar, vai  retornar essa mensagem
    except json.JSONDecodeError:  # caso contrário:
        print("Não foi possível decodificar a mensagem como JSON.")

client = mqtt.Client() # essa linha instancia um objeto da classe client, da bliblioteca paho, vai ser utilizado para se conectar ao broker, se inscrever em tópicos, reagir mensagens, etc...
client.username_pw_set("sofia", "Tatimari13") #aqui estou configurando as credenciais para autenticação com o broker, como se estivesse falando "oi broker, é a sofia e minha senha é tatimari13, posso entrar?" :D
client.on_connect = on_connect # atribuição da callback, toda vez que o cliente se conectar ao broker, essa função será chamada.
client.on_message = on_message # atribuição da callback também, quando uma mensagem for recebida, essa função será chamada.  
client.connect("localhost", 1883, 60) # esse método conecta ao broker
client.loop_forever() # mantém o cliente rodando para sempre.
