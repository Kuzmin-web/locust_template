from locust import task, SequentialTaskSet, HttpUser, constant_pacing, events, FastHttpUser
import sys
from config.config import cfg, logger



class PurchaseFlightTicket(SequentialTaskSet): # класс с задачами (содержит основной сценарий)
    @task()
    def uc_00_getHomePage(self):
        r00_01_response = self.client.get(
            '/WebTours/',
            name="r00_01_response",
            allow_redirects=False,
            headers={
                'sec-ch-ua': '"Google Chrome";v="143", "Chromium";v="143", "Not A(Brand";v="24"',
                'sec-ch-ua-mobile': '?0'
            },
            debug_stream=sys.stderr
        )


        r00_02_header_html = self.client.get(
            '/WebTours/header.html',
            name="r00_02_header_html",
            allow_redirects=False,
            debug_stream=sys.stderr
        )
        

        r00_03_welcome_pl = self.client.get(
            '/cgi-bin/welcome.pl?signOff=true',
            name="r00_03_welcome_pl_html",
            allow_redirects=False,
            debug_stream=sys.stderr
        )


        r00_04_navi_pl = self.client.get(
            '/cgi-bin/nav.pl?in=home',
            name="r00_04_navi_pl",
            allow_redirects=False,
            debug_stream=sys.stderr
        )


        r00_05_home_html = self.client.get(
            '/cgi-bin/nav.pl?in=home',
            name="r00_05_home_html",
            allow_redirects=False,
            debug_stream=sys.stderr
        )       


        # logger.info(f"Статус ответа: {r00_01_response.status_code}, Тело ответа {r00_01_response.text}")
        # print(f"Статус ответа: {r00_01_response.status_code}, Тело ответа {r00_01_response.text}")
        

class WebToursBaseUserClass(FastHttpUser): # юзер-класс, принимающий в себя основные параметры теста
    wait_time = constant_pacing(cfg.pacing)
    host = cfg.url

    tasks = [PurchaseFlightTicket]