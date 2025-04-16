import paho.mqtt.client as mqtt 
import time 
import json 

client = mqtt.Client()    
client.username_pw_set("admin", "Tatimari13")  
broker_address = "localhost" 

mensagem = {   
    "dispositivo": "sensor_1",
    "temperatura": 23.7,
    "umidade": 61,
    "status": "ativo",
    "timestamp": time.time() 
}

mensagem_json = json.dumps(mensagem) 

client.publish("metam/admin", mensagem_json) 

time.sleep(1) 
