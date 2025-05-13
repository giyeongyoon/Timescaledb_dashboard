import paho.mqtt.client as mqtt
from postgresql import get_conn_db
from datetime import datetime, timezone

broker_address = "172.30.1.8"
topic = "lora32_vwc"

postgres_db = get_conn_db()
db_cursor = postgres_db.cursor()

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("브로커에 성공적으로 연결되었습니다!")
        client.subscribe(topic)
    else:
        print(f"연결 실패! 반환코드: {rc}")

def on_message(client, userdata, message):
    moisture = float(message.payload.decode())
    sensor_id = 'TEROS10'

    sql = "INSERT INTO soil_moisture (sensor_id, moisture) VALUES (%s, %s);"
    # print(sql)
    db_cursor.execute(sql, (sensor_id, moisture))
    postgres_db.commit()
    print(f"Saved: {sensor_id} -> {moisture}")
    

def run():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(broker_address)
    client.loop_forever()


if __name__ == "__main__":
    run()