import yagmail
from common.config import conf

def send_email(**kwargs):
    moisture = kwargs.get("moisture")
    sensor_id = kwargs.get("sensor_id")
    status = kwargs.get("status")
    email_addr = conf["email"]
    email_pw = conf["email_pw"]
    try:
        yag = yagmail.SMTP(user=email_addr, password=email_pw)
        subject = "토양수분 이상치 감지지"
        contents=f"""
            [경고 알림]
            비정상 수분 수치가 감지되었습니다.

            - 센서: {sensor_id}
            - 수분: {moisture}%
            - 상태: {status}

            주의가 필요합니다.
        """
        yag.send(to=email_addr, subject=subject, contents=contents)
    except Exception as e:
        print(e)