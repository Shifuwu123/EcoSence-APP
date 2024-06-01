
def mqtt_connect(client, broker, topic):
        try:
            client.connect(broker)  # Conectar al broker MQTT
            client.subscribe(topic) # Suscribirse a todos los tópicos bajo 'EcoSense/esp32/'
            client.loop_start() # Iniciar el loop de MQTT en segundo plano
            print(f"Conectado al broker MQTT '{broker}' al topic: '{topic}'")

        except Exception as e:
            print(f"ERROR al conectar al broker MQTT: {e}")
            return False

        return client