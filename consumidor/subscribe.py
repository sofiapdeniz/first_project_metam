import paho.mqtt.client as mqtt
import json
import mysql.connector # esse módulo serve para tratar os erros de uma forma mais elegante kk

# precisamos fazer uma função que será chamada quando a conexão com o broker for estabelecida, o paho chama automaticamente quando o client conecta ao broker
def on_connect(client, userdata, flags, rc): #userdata e flags são parâmetros que não estaremos utilizando agora, portanto, o paho espera a assinatura correta, que são esses 4 argumentos, o python aceita tirar mas a biblioteca espera ter esses 4, pra não dar erro deixamos :) lembrando que existem maneiras de esconder, mas vamos deixar assim quietin
    print("Conectado com código de retorno:", rc) #rc significa "return code", indica se a conexão foi bem sucedida, deve retornar 0, se retornar outro valor está errado.
    client.subscribe("metam/admin") #aqui se inscrevemos no tópico, o cliente vai ouvir mensagens desse tópico.

# def on_message e def on_connect são callbacks da biblioteca paho, padrão mesmo, essa serve para cada vez que uma mensagem chega no tópico que estamos, é chamada.
def on_message(client, userdata, msg):
    print("Mensagem recebida no tópico:", msg.topic, flush="True") # exibe o nome do tópico que recebeu a mensagem
    print("Conteúdo da Mensagem (raw):", msg.payload.decode(), flush="True") # "msg.payloadé o conteúdo da msg mas em bytes, decode transforma de bytes para str(utf-8), então a mensagem vai chegar crua.
    

    try: # TENTA interpretar a string da msg como JSON e transformar em um dicionário python (linha abaixo)
        dados = json.loads(msg.payload.decode())
        print("JSON decodificado:", dados, flush="True") # se rolar, vai  retornar essa mensagem

        conexao = mysql.connector.connect( # aqui estamos fazendo a conexão do subscribe com o banco, bem simples, depois passamos todas as informações:
            host='mysql_data', # aqui o host :)
            database='mysql_db', # aqui é o banco, nome do banco :)
            user='m_user', # nosso querido e idolatrado user
            password='m_pass' # nossa querida e idolatrada senha
        )

        if conexao.is_connected(): # "se a conexao está conectada" verifica se a conexao deu certo :DD
            cursor = conexao.cursor() # cria o cursor, como se fosse um ponteiro, para executar comandos SQL dentro do banco.

#aqui definimos o comando SQL que será executado, %s são placeholders, lugar onde mais tarde serão armazenados valores, os valores não são passados agora pois, pode dar SQL injection.
            comando = """  
               INSERT INTO leituras (dispositivo, temperatura, umidade, status, timestamp)
               VALUES (%s, %s, %s, %s, %s)
            """

# aqui extraimos do dicionário dados que vieram da msg MQTT os valores que vamos inserir no banco, eles precisam estar na mesma ordem do SQL:
            valores = (
                dados["dispositivo"],
                dados["temperatura"],
                dados["umidade"],
                dados["status"],
                dados["timestamp"]
            )

            cursor.execute(comando, valores) # aqui de fato o comando é executado com os valores, esse cursor vai enviar esse comando para o MySQL
            conexao.commit() # no MySQL, comandos de escrita precisam ser configurados com commit, se não eles não vão ficar salvos de verdade no banco.
            print("Dados inseridos com sucesso no MySQL!", flush="True")

    except mysql.connector.Error as erro: # se algum erro acontecer na conexão ou inserção, esse bloco irá capturar o erro e retornar a msg abaixo, isso evita que o programa quebre com erro feio no terminal.
        print("Erro ao conectar ou inserir no MySQL:", erro, flush="True")

    finally: # esse FINALMENTE, sempre roda, até se der erro, ele vai fechar o cursor, fechar a conexão com o banco e mostrar que tudo foi finalizado certin
        if 'conexao' in locals() and conexao.is_connected():
            cursor.close()
            conexao.close()
            print("Conexão com MySQL encerrada.", flush="True")

client = mqtt.Client() # essa linha instancia um objeto da classe client, da bliblioteca paho, vai ser utilizado para se conectar ao broker, se inscrever em tópicos, reagir mensagens, etc...
# client.username_pw_set("admin", "Tatimari13") #aqui estou configurando as credenciais para autenticação com o broker, como se estivesse falando "oi broker, é a sofia e minha senha é tatimari13, posso entrar?" :D
client.on_connect = on_connect # atribuição da callback, toda vez que o cliente se conectar ao broker, essa função será chamada.
client.on_message = on_message # atribuição da callback também, quando uma mensagem for recebida, essa função será chamada.  
client.connect("emqx", 1883, 60) # esse método conecta ao broker
client.loop_forever() # mantém o cliente rodando para sempre.

#insert manual:
#INSERT INTO leituras (dispositivo, temperatura, umidade, status, timestamp)
#VALUES ('sensor_1', 23.7, 60, 'ativo', 1744636936);

