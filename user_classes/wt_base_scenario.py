from locust import task, SequentialTaskSet, HttpUser, constant_pacing, events, FastHttpUser
import sys, re, random
from config.config import cfg, logger
from utils.assertion import check_http_response
from utils.non_test_methods import open_csv_file, open_random_csv_file

class PurchaseFlightTicket(SequentialTaskSet): # класс с задачами (содержит основной сценарий)

    def on_start(self):
        self.user_data_csv_file = './test_data/login,password,address1,address2,pass1,arrive,depart.csv'
        self.user_data = open_csv_file(self.user_data_csv_file)
        self.random_user_data = open_random_csv_file(self.user_data_csv_file)
        # logger.info(f"__________SPISOK POLZOVATELEY: {self.random_user_data}")

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
            # debug_stream=sys.stderr,
            catch_response=True
        ) as r00_01_response:
            check_http_response(r00_01_response, "Web Tours")


        with self.client.get(
            '/WebTours/header.html',
            name="r00_02_header_html",
            allow_redirects=False,
            # debug_stream=sys.stderr,
            catch_response=True
        ) as r00_02_header_html:
            check_http_response(r00_02_header_html, "images/webtours.png")
        
        check = "Web Tours"

        with self.client.get(
            '/cgi-bin/welcome.pl?signOff=true',
            name="r00_03_welcome_pl_html",
            allow_redirects=False,
            # debug_stream=sys.stderr,
            catch_response=True 
        ) as r00_03_welcome_pl_html:
            check_http_response(r00_03_welcome_pl_html, f'{check}')


        with self.client.get(
            '/cgi-bin/nav.pl?in=home',
            name="r00_04_navi_pl",
            allow_redirects=False,
            # debug_stream=sys.stderr,
            catch_response=True
        ) as r00_04_navi_pl:
            check_http_response(r00_04_navi_pl, "Web Tours Navigation Bar")

        self.user_session = re.search(r'name="userSession" value="(.+?)"', r00_04_navi_pl.text).group(1)

        with self.client.get(
            '/WebTours/home.html',
            name="r00_05_home_html",
            allow_redirects=False,
            # debug_stream=sys.stderr,
            catch_response=True
        ) as r00_05_home_html:
            check_http_response(r00_05_home_html, "Welcome to the Web Tours site")

    @task()
    def uc_01_login(self):
       
        self.users_row = next(self.user_data)
        self.random_user_row = random.choice(self.random_user_data)
        print(f"DEBUG: KEYS: {self.random_user_row.keys()}") # Это покажет реальные имена колонок
        self.login = self.random_user_row["login"]
        self.password = self.random_user_row["password"]

        self.body_r01_01_login_pl = f'userSession={self.user_session}&username={self.login}&password={self.password}&login.x=53&login.y=6&JSFormSubmit=off'
        
        print(f"______________BODY LOGIN: {self.body_r01_01_login_pl}")
        logger.info(f"______________BODY LOGIN: {self.body_r01_01_login_pl}")

        with self.client.post(
            '/cgi-bin/login.pl',
            name="r01_01_login.pl",
            allow_redirects=False,
            headers={'content-type': 'application/x-www-form-urlencoded'},
            data=self.body_r01_01_login_pl,
            # debug_stream=sys.stderr,
            catch_response=True
        ) as r01_01_login_pl:
            check_http_response(r01_01_login_pl, "Web Tours")

        with self.client.get(
            '/cgi-bin/nav.pl?in=home',
            name="r01_02_nav_pl",
            allow_redirects=False,
            # debug_stream=sys.stderr,
            catch_response=True
        ) as r01_02_nav_pl:
            check_http_response(r01_02_nav_pl, "Web Tours Navigation Bar")

    
        with self.client.get(
            '/cgi-bin/login.pl?intro=true',
            name="r01_03_login_pl",
            allow_redirects=False,
            debug_stream=sys.stderr,
            catch_response=True
        ) as r01_03_login_pl:
            check_http_response(r01_03_login_pl, f"Welcome, <b>{self.login}</b>")



        # logger.info(f"Статус ответа: {r00_01_response.status_code}, Тело ответа {r00_01_response.text}")
        # print(f"Статус ответа: {r00_01_response.status_code}, Тело ответа {r00_01_response.text}")
        

class WebToursBaseUserClass(FastHttpUser): # юзер-класс, принимающий в себя основные параметры теста
    wait_time = constant_pacing(cfg.pacing)
    host = cfg.url

    tasks = [PurchaseFlightTicket]