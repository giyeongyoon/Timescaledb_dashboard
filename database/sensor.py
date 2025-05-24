# dashboard/database/sensor.py
import paho.mqtt.client as mqtt
from postgresql import get_conn_db
from common.consts import mqtt_info
from function.notification import send_email
from common.logging_config import setup_logging
import logging

setup_logging()
logger = logging.getLogger(__name__)

broker_address = mqtt_info.get('broker_address')
topic = mqtt_info.get('topic')
last_alert_state = None

postgres_db = get_conn_db()
db_cursor = postgres_db.cursor()

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        logger.info("브로커에 성공적으로 연결되었습니다!")
        client.subscribe(topic)
    else:
        logger.info(f"연결 실패! 반환코드: {rc}")

def on_message(client, userdata, message):
    global last_alert_state

    moisture = float(message.payload.decode())
    sensor_id = 'TEROS10'

    if moisture < 19:
        current_state = "too_dry"
    elif moisture > 24:
        current_state = "too_wet"
    else:
        current_state = "normal"
    
    if current_state != last_alert_state and current_state != "normal":
        send_email(moisture=moisture, 
                   sensor_id=sensor_id, 
                   status=current_state)

    last_alert_state = current_state

    try:
        sql = "INSERT INTO soil_moisture (sensor_id, moisture) VALUES (%s, %s);"
        db_cursor.execute(sql, (sensor_id, moisture))
        postgres_db.commit()
        # print(f"Saved: {sensor_id} -> {moisture}")
    except Exception as e:
        logger.error(f"DB 저장 실패: {e}", exc_info=True)
    

def run():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(broker_address)
    client.loop_forever()


if __name__ == "__main__":
    run()