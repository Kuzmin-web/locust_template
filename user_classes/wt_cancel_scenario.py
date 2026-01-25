from locust import task, SequentialTaskSet, HttpUser, constant_pacing, events, FastHttpUser
import sys, re, random
from config.config import cfg, logger
from utils.assertion import check_http_response
from utils.non_test_methods import open_csv_file, open_random_csv_file, generateFlightDate, processCancelRequestBody
from urllib.parse import quote_plus

class Cancel(SequentialTaskSet): # класс с задачами (содержит основной сценарий)

    def on_start(self):
        self.user_data_csv_file = './test_data/login,password,address1,address2,pass1,arrive,depart.csv'
        self.flights_deatails_csv_file = './test_data/expDate,creditCard,seatType,seatPref.csv'
        self.user_data = open_csv_file(self.user_data_csv_file)
        self.random_user_data = open_random_csv_file(self.user_data_csv_file)
        self.random_flight_data = open_random_csv_file(self.flights_deatails_csv_file)
        # logger.info(f"__________SPISOK POLZOVATELEY: {self.random_user_data}")

        # Прогрев сервера для снижения cold start задержки
        try:
            self.client.get('/WebTours/', allow_redirects=False, catch_response=True, name='warmup')
        except:
            pass

        with self.client.get(
            '/WebTours/',
            name="r00_01_response",
            allow_redirects=False,
            catch_response=True,
            headers={
                'sec-ch-ua': '"Not A(Brand";v="99", "Google Chrome";v="121"',
                'sec-ch-ua-mobile': '?0'
            }
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

        self.users_row = next(self.user_data)
        self.random_user_row = random.choice(self.random_user_data)  # Выбираем случайного пользователя из CSV файла
        # print(f"DEBUG: KEYS: {self.random_user_row.keys()}") # Это покажет реальные имена колонок
        self.login = self.random_user_row["login"]
        self.password = self.random_user_row["password"]
        self.headers = {
            'content-type': 'application/x-www-form-urlencoded'
        }

        self.body_r01_01_login_pl = f'userSession={self.user_session}&username={self.login}&password={self.password}&login.x=53&login.y=6&JSFormSubmit=off'
        
        # print(f"______________BODY LOGIN: {self.body_r01_01_login_pl}")
        # logger.info(f"______________BODY LOGIN: {self.body_r01_01_login_pl}")

        with self.client.post(
            '/cgi-bin/login.pl',
            name="r01_01_login.pl",
            allow_redirects=False,
            headers=self.headers,
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
            # debug_stream=sys.stderr,
            catch_response=True
        ) as r01_03_login_pl:
            check_http_response(r01_03_login_pl, f"Welcome, <b>{self.login}</b>")
        
        
    @task               
    def uc_06_Itinerary(self):
        with self.client.get(
            '/cgi-bin/welcome.pl?page=itinerary',
            name="r06_01_welcome.pl?page=itinerary",
            allow_redirects=False,
            # debug_stream=sys.stderr,
            catch_response=True
        ) as r06_01_welcome_pl_itinerary:
            check_http_response(r06_01_welcome_pl_itinerary, "User wants the intineraries")
            
        
        with self.client.get(
            '/cgi-bin/nav.pl?page=menu&in=itinerary',
            name="r06_02_nav.pl?page=menu&in=itinerary",
            allow_redirects=False,
            # debug_stream=sys.stderr,
            catch_response=True
        ) as r06_02_nav_pl_itinerary:
            check_http_response(r06_02_nav_pl_itinerary, "Web Tours Navigation Bar")
        
        
        with self.client.get(
            '/cgi-bin/itinerary.pl',
            name="r06_03_itinerary.pl",
            allow_redirects=False,
            # debug_stream=sys.stderr,
            catch_response=True
        ) as r06_03_itinerary_pl:
            check_http_response(r06_03_itinerary_pl, "Flights List")
            
        self.flight_ids= re.findall(r'<input type="hidden" name="flightID" value="([^"]*)"', r06_03_itinerary_pl.text)
        self.flight_nums = re.findall(r'<input type="checkbox" name="([0-9]{1,4})" value="on"', r06_03_itinerary_pl.text)
        
        # logger.info(f"__________SPISOK FLIGHT IDS: {self.flight_ids}")
        # logger.info(f"__________SPISOK FLIGHT NUMS: {self.flight_nums}")
    
    
    @task               
    def uc_07_DeleteOneTicket(self):
    
        if self.flight_ids:    
        
            data_r07_01_itinerary_pl_DeleteOneTicket = processCancelRequestBody(self.flight_ids, self.flight_nums)
        
            with self.client.post(
                '/cgi-bin/itinerary.pl',
                name="r07_01_itinerary_pl_DeleteOneTicket",
                headers=self.headers,
                allow_redirects=False,
                data=data_r07_01_itinerary_pl_DeleteOneTicket,
                # debug_stream=sys.stderr,
                catch_response=True
            ) as r07_01_itinerary_pl_DeleteOneTicket:
                check_http_response(r07_01_itinerary_pl_DeleteOneTicket, "Flights List")
        
        else:
            logger.info(f"No Tickets for user {self.login}.")        

class WebToursCancelUserClass(HttpUser): # юзер-класс, принимающий в себя основные параметры теста
    wait_time = constant_pacing(cfg.pacing)
    host = cfg.url
    tasks = [Cancel]