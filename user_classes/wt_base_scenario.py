from locust import task, SequentialTaskSet, HttpUser, constant_pacing, events, FastHttpUser
from config.config import cfg, logger
import sys


class PurchaseFlightTicket(SequentialTaskSet): # класс с задачами (содержит основной сценарий)
    @task()
    def uc_00_getHomePage(self):
        r00_01_responce = self.client.get(
            '/WebTours/',
            name="r00_01_responce",
            allow_redirects=False,
            headers={
                'sec-ch-ua': '"Google Chrome";v="143", "Chromium";v="143", "Not A(Brand";v="24"',
                'sec-ch-ua-mobile': '?0'
            },
            debug_stream=sys.stdout
        )
        logger.info(f"Статус ответа: {r00_01_responce.status_code}, Тело ответа {r00_01_responce.text}")
        # print(f"Статус ответа: {r00_01_responce.status_code}, Тело ответа {r00_01_responce.text}")
        

class WebToursBaseUserClass(HttpUser): # юзер-класс, принимающий в себя основные параметры теста
    wait_time = constant_pacing(cfg.pacing)
    host = cfg.url

    tasks = [PurchaseFlightTicket]