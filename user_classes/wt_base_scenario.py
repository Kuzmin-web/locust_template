from locust import task, SequentialTaskSet, HttpUser, constant_pacing, events, FastHttpUser
import sys, re, random
from config.config import cfg, logger
from utils.assertion import check_http_response
from utils.non_test_methods import open_csv_file, open_random_csv_file, generateFlightDate
from urllib.parse import quote_plus

class PurchaseFlightTicket(SequentialTaskSet): # класс с задачами (содержит основной сценарий)

    def on_start(self):
        self.user_data_csv_file = './test_data/login,password,address1,address2,pass1,arrive,depart.csv'
        self.flights_deatails_csv_file = './test_data/expDate,creditCard,seatType,seatPref.csv'
        self.user_data = open_csv_file(self.user_data_csv_file)
        self.random_user_data = open_random_csv_file(self.user_data_csv_file)
        self.random_flight_data = open_random_csv_file(self.flights_deatails_csv_file)
        # logger.info(f"__________SPISOK POLZOVATELEY: {self.random_user_data}")

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


    @task()
    def uc_02_Check_Flights(self):

        with self.client.get(
            '/cgi-bin/welcome.pl?page=search',
            name="r02_01_welcome_pl",
            allow_redirects=False,
            # debug_stream=sys.stderr,
            catch_response=True
        ) as r02_01_welcome_pl:
            check_http_response(r02_01_welcome_pl, "Web Tours")


        with self.client.get(
            '/cgi-bin/nav.pl?page=menu&in=flights',
            name="r02_02_menu_flights_pl",
            allow_redirects=False,
            # debug_stream=sys.stderr,
            catch_response=True
        ) as r02_02_menu_flights_pl:
            check_http_response(r02_02_menu_flights_pl, "Web Tours Navigation Bar")


        with self.client.get(
            '/cgi-bin/reservations.pl?page=welcome',
            name="r02_03_reservations_welcome_pl",
            allow_redirects=False,
            # debug_stream=sys.stderr,
            catch_response=True
        ) as r02_03_reservations_welcome_pl:
            check_http_response(r02_03_reservations_welcome_pl, "Flight Selections")
            
            
    @task()
    def uc_03_Find_Flight(self):
        
        self.random_flights_row = random.choice(self.random_flight_data) # Выбираем случайные данные по рейсам из CSV файла 
        self.depart = self.random_user_row["depart"]
        self.arrive = self.random_user_row["arrive"]
        self.seatType = self.random_flights_row["seatType"]
        self.seatPref = self.random_flights_row["seatPref"]
        
        self.departDate, self.returnDate = generateFlightDate()
        
        # logger.info(f"______________DEPART DATE: {self.departDate}, RETURN DATE: {self.returnDate}")

        self.body_r03_01_reservations_pl = f'advanceDiscount=0&depart={self.depart}&departDate={self.departDate}&arrive={self.arrive}&returnDate={self.returnDate}&numPassengers=1&seatPref={self.seatPref}&seatType={self.seatType}&findFlights.x=49&findFlights.y=9&.cgifields=roundtrip&.cgifields=seatType&.cgifields=seatPref'
        # logger.info(f"______________DATA_R03_01: {self.body_r03_01_reservations_pl}")  
  
        with self.client.post(
            '/cgi-bin/reservations.pl',
            name="r03_01_reservations_pl",
            data=self.body_r03_01_reservations_pl,
            headers=self.headers,
            allow_redirects=False,
            # debug_stream=sys.stderr,
            catch_response=True
        ) as r03_01_reservations_pl:
            check_http_response(r03_01_reservations_pl, "Flight Selections")
            
        self.dict_outboundFlight = re.findall(r'name="outboundFlight"\s+value="([^"]*)"', r03_01_reservations_pl.text)
        
        # logger.info(f"______________SELECTED FLIGHT: {self.dict_outboundFlight}")
    
    
    @task()
    def uc_04_ChiooseFlightsOptions(self):
        
        self.seatType = self.random_flights_row["seatType"]
        self.seatPref = self.random_flights_row["seatPref"]
        
        self.outboundFlight = random.choice(self.dict_outboundFlight)

        self.body_uc_04_01_ChiooseFlightsOptions = f'outboundFlight={self.outboundFlight}&numPassengers=1&advanceDiscount=0&seatType={self.seatType}&seatPref={self.seatPref}&reserveFlights.x=57&reserveFlights.y=10'

        # logger.info(f"______________DATA_uc_04_01_ChiooseFlightsOptions: {self.body_uc_04_01_ChiooseFlightsOptions}")
         
        with self.client.post(
            '/cgi-bin/reservations.pl',
            name="uc_04_01_ChiooseFlightsOptions",
            data=self.body_uc_04_01_ChiooseFlightsOptions,
            headers=self.headers,
            allow_redirects=False,
            # debug_stream=sys.stderr,
            catch_response=True
        ) as uc_04_01_ChiooseFlightsOptions:
            check_http_response(uc_04_01_ChiooseFlightsOptions, "Flight Reservation")        

            
    @task()
    def uc_05_PaymentDetails(self):
        
        self.creditCard = self.random_flights_row["creditCard"]
        self.expDate = self.random_flights_row["expDate"]
        self.adress1 = self.random_user_row["address1"]
        self.adress2 = self.random_user_row["address2"]
        self.pass1 = self.random_user_row["pass1"]

        self.body_uc_05_01_PaymentDetails = f'firstName={self.login}&lastName={self.password}&address1={self.adress1}&address2={self.adress2}&pass1=jojo+bean&creditCard={self.creditCard}&expDate={self.expDate}&oldCCOption=&numPassengers=1&seatType={self.seatType}&seatPref={self.seatPref}&outboundFlight={self.outboundFlight}&advanceDiscount=0&returnFlight=&JSFormSubmit=off&buyFlights.x=76&buyFlights.y=11&.cgifields=saveCC'

        # logger.info(f"______________DATA_uc_05_01_PaymentDetails: {self.body_uc_05_01_PaymentDetails}")
         
        with self.client.post(
            '/cgi-bin/reservations.pl',
            name="uc_05_01_PaymentDetails",
            data=self.body_uc_05_01_PaymentDetails,
            headers=self.headers,
            allow_redirects=False,
            # debug_stream=sys.stderr,
            catch_response=True
        ) as uc_05_01_PaymentDetails:
            check_http_response(uc_05_01_PaymentDetails, "Thank you for booking through Web Tours.")                        
            
        

        # logger.info(f"Статус ответа: {r00_01_response.status_code}, Тело ответа {r00_01_response.text}")
        # print(f"Статус ответа: {r00_01_response.status_code}, Тело ответа {r00_01_response.text}")
        

class WebToursBaseUserClass(FastHttpUser): # юзер-класс, принимающий в себя основные параметры теста
    wait_time = constant_pacing(cfg.pacing)
    host = cfg.url
    tasks = [PurchaseFlightTicket]

    tasks = [PurchaseFlightTicket]