import paho.mqtt.client as mqtt
import json
import mysql.connector 

def on_connect(client, userdata, flags, rc): 
    print("Conectado com código de retorno:", rc, flush="True")
    client.subscribe("metam/admin") 

def on_message(client, userdata, msg):
    print("Mensagem recebida no tópico:", msg.topic, flush="True") 
    print("Conteúdo da Mensagem (raw):", msg.payload.decode(), flush="True") 
    

    try: 
        dados = json.loads(msg.payload.decode())
        print("JSON decodificado:", dados, flush="True") 

        conexao = mysql.connector.connect( 
            host='mysql_data', 
            database='mysql_db', 
            user='m_user', 
            password='m_pass' 
        )

        if conexao.is_connected(): 
            cursor = conexao.cursor() 

            comando = """  
               INSERT INTO leituras (dispositivo, temperatura, umidade, status, timestamp)
               VALUES (%s, %s, %s, %s, %s)
            """

            valores = (
                dados["dispositivo"],
                dados["temperatura"],
                dados["umidade"],
                dados["status"],
                dados["timestamp"]
            )

            cursor.execute(comando, valores) 
            conexao.commit() 

    except mysql.connector.Error as erro: 
        print("Erro ao conectar ou inserir no MySQL:", erro, flush="True")

    finally:
        if 'conexao' in locals() and conexao.is_connected():
            cursor.close()
            conexao.close()
            print("Conexão com MySQL encerrada.", flush="True")

client = mqtt.Client() 
client.on_connect = on_connect 
client.on_message = on_message 
client.connect("emqx", 1883, 60) 
client.loop_forever() 


