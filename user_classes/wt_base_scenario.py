from locust import task, SequentialTaskSet, HttpUser, constant_pacing, events, FastHttpUser
import sys
from config.config import cfg, logger
from utils.assertion import check_http_response 


class PurchaseFlightTicket(SequentialTaskSet): # класс с задачами (содержит основной сценарий)
    @task()
    def uc_00_getHomePage(self):
        with self.client.get(
            '/WebTours/',
            name="r00_01_response",
            allow_redirects=False,
            headers={
                'sec-ch-ua': '"Google Chrome";v="143", "Chromium";v="143", "Not A(Brand";v="24"',
                'sec-ch-ua-mobile': '?0'
            },
            debug_stream=sys.stderr,
            catch_response=True
        ) as r00_01_response:
            check_http_response(r00_01_response, "Web Tours")


        with self.client.get(
            '/WebTours/header.html',
            name="r00_02_header_html",
            allow_redirects=False,
            debug_stream=sys.stderr,
            catch_response=True
        ) as r00_02_header_html:
            check_http_response(r00_02_header_html, "images/webtours.png")
        

        with self.client.get(
            '/cgi-bin/welcome.pl?signOff=true',
            name="r00_03_welcome_pl_html",
            allow_redirects=False,
            debug_stream=sys.stderr,
            catch_response=True 
        ) as r00_03_welcome_pl_html:
            check_http_response(r00_03_welcome_pl_html, "Welcome to Web Tours")


        with self.client.get(
            '/cgi-bin/nav.pl?in=home',
            name="r00_04_navi_pl",
            allow_redirects=False,
            debug_stream=sys.stderr,
            catch_response=True
        ) as r00_04_navi_pl:
            check_http_response(r00_04_navi_pl, "Web Tours")


        with self.client.get(
            '/cgi-bin/nav.pl?in=home',
            name="r00_05_home_html",
            allow_redirects=False,
            debug_stream=sys.stderr,
            catch_response=True
        ) as r00_05_home_html:
            check_http_response(r00_05_home_html, "Web Tours")


        # logger.info(f"Статус ответа: {r00_01_response.status_code}, Тело ответа {r00_01_response.text}")
        # print(f"Статус ответа: {r00_01_response.status_code}, Тело ответа {r00_01_response.text}")
        

class WebToursBaseUserClass(FastHttpUser): # юзер-класс, принимающий в себя основные параметры теста
    wait_time = constant_pacing(cfg.pacing)
    host = cfg.url

    tasks = [PurchaseFlightTicket]