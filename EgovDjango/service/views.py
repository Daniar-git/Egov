import time
from urllib.parse import urlparse, parse_qs

import requests

from rest_framework import views, status
from selenium import webdriver
from rest_framework.response import Response
from selenium.webdriver.common.by import By


class FormaView(views.APIView):
    def post(self, request):
        s = requests.Session()
        cookies = request.data.get('cookies')
        for cookie_name, cookie_value in cookies.items():
            s.cookies.set(cookie_name, cookie_value)
        time.sleep(3)
        print(s.cookies)
        s.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'
        s.headers['Host'] = 'egov.kz'
        s.headers['Origin'] = None
        s.headers['Referer'] = None
        s.get('https://egov.kz/cms/ru/services/buy_sale/pass076_mu')
        res = s.get('https://egov.kz/services/P3.05/#/declaration/0//')
        print(res.status_code)
        res = s.get('https://egov.kz/services/P80.01/rest/current-user')
        user_data = res.json()
        payload = {
            "relationship": "SELF",
            "declarantUin": user_data.get('uin'),
            "childUin": None,
            "objectTypeId": "3",
            "documentTypeId": "002",
            "address": "1000000000000173263",
            "house": "1",
            "housing": None,
            "apartment": None,
            "garage": None,
            "countryHouse": None
        }
        s.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'
        s.headers['Accept-Encoding'] = 'gzip, deflate'
        s.headers['Accept'] = 'application/json, text/plain, */*'
        s.headers['Connection'] = 'keep-alive'
        s.headers['Host'] = 'egov.kz'
        s.headers['Origin'] = 'https://egov.kz'
        s.headers['Referer'] = 'https://egov.kz/services/P3.05/'
        s.headers['Sec-Fetch-Mode'] = 'cors'
        s.headers['Sec-Fetch-Site'] = 'same-origin'
        s.headers['Content-Type'] = 'application/json'
        print(user_data.get('uin'))
        res = s.options("https://egov.kz/services/P3.05/rest/app/get-signing-url", data=payload)
        res = s.head("https://egov.kz/services/P3.05/rest/app/get-signing-url", data=payload)
        print(res.status_code)
        res = s.head('https://egov.kz/services/signing/rest/otp/generate?uin=040705550178')
        print(res)
        return Response({"status": "True"}, status=200)


# class FormaCredentialsView(views.APIView):
#     def post(self, request):
#         cookies = request.data.get('cookies')
#
        # options = webdriver.FirefoxOptions()
        # browser = webdriver.Firefox(options=options)
        # browser.get("https://egov.kz/")
        # for name, value in cookies.items():
        #     cookie_dict = {
        #         "name": name,
        #         "value": value,
        #     }
        #     browser.add_cookie(cookie_dict)
        # browser.refresh()
        #
        # browser.get('https://egov.kz/services/P3.05/#/declaration/0/030703550889,,SELF/')
        # time.sleep(3)
        # type_object = browser.find_element(By.XPATH, '//*[@id="search"]/div/div/div/div[3]/div/div/div/div')
        # type_object.click()
        #
        # time.sleep(2)
        #
        # select_type = browser.find_element(By.XPATH,
        #                                    '/html/body/div[4]/div[1]/div/div[1]/article/div/div/div/div/ul/li[4]')
        # select_type.click()
        #
        # time.sleep(2)
        #
        # adress = browser.find_element(By.XPATH, '//*[@id="search"]/div/div/div/div[5]/div/div/textarea')
        # adress.click()
        #
        # time.sleep(2)
        #
        # area = browser.find_element(By.XPATH,'/html/body/div[6]/div[1]/div/div[1]/article/div[1]/div/div/div/div/div/div')
        # area.click()
        #
        # time.sleep(2)
        #
        # areaclick = browser.find_element(By.XPATH,
        #                                  '/html/body/div[7]/div[1]/div/div[1]/article/div/div/div[2]/div/ul/li[6]')
        # areaclick.click()
        #
        # time.sleep(2)
        #
        # region = browser.find_element(By.XPATH, '/html/body/div[6]/div[1]/div/div[1]/article/div[1]/div[2]/div/div/div/div/div')
        # region.click()
        #
        # time.sleep(2)
        #
        # regionclick = browser.find_element(By.XPATH, '/html/body/div[8]/div[1]/div/div[1]/article/div/div/div/div/ul/li[4]')
        # regionclick.click()
        #
        # time.sleep(2)
        #
        # street = browser.find_element(By.XPATH, '/html/body/div[6]/div[1]/div/div[1]/article/div[1]/div[3]/div/div/div/div/div')
        # street.click()
        #
        # time.sleep(2)
        #
        # streetclick = browser.find_element(By.XPATH, '/html/body/div[9]/div[1]/div/div[1]/article/div/div/div[2]/div/ul/li[8]')
        # streetclick.click()
        #
        # time.sleep(2)
        #
        # savebutton = browser.find_element(By.XPATH, '/html/body/div[6]/div[1]/div/footer/div[2]/button')
        # savebutton.click()
        #
        # time.sleep(2)
        #
        # dom = browser.find_element(By.XPATH,
        #                            '//*[@id="search"]/div/div/div/div[5]/fieldset/table/tbody/tr[1]/td/div/input')
        # dom.send_keys('12/1')
        #
        # time.sleep(2)
        #
        # send = browser.find_element(By.XPATH, '//*[@id="searchSignButton"]')
        # send.click()
        #
        # time.sleep(4)
        #
        # browser.find_element(By.XPATH, '//*[@id="sign"]/div/div/div/div[1]/div/button[1]').click()
        #
        # time.sleep(6)
        #
        # get_code = browser.find_element(By.XPATH, '//*[@id="sign"]/div/div/div/div[3]/div/div/div/fieldset/div[2]/button')
        # get_code.click()
        #
        # time.sleep(1)
        #
        # response = {
        #     "current_url": browser.current_url,
        #     "cookies": browser.get_cookies()
        # }

        # return Response(response, status=200)


class FormaCodeView(views.APIView):
    def post(self, request):
        url = request.data.get('current_url')
        cookies = request.data.get('cookies')
        s = requests.Session()
        code = request.data.get('code')
        for cookie_dict in cookies:
            s.cookies.set(
                name=cookie_dict['name'],
                value=cookie_dict['value'],
                domain=cookie_dict['domain'],
                path=cookie_dict['path']
            )
        s.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'
        s.headers['Host'] = 'egov.kz'
        s.headers['Origin'] = None
        s.headers['Referer'] = None
        s.get('https://egov.kz/cms/ru/services/buy_sale/pass076_mu')
        s.get('https://egov.kz/services/P3.05/#/declaration/0//')
        res = s.get('https://egov.kz/services/P80.01/rest/current-user')
        print(res.text)
        result = s.get(url)
        print(result.status_code)
        parsed_url = urlparse(url)
        query_parameters = parse_qs(parsed_url.query)
        page_query_id = query_parameters.get('PageQueryID', [])[0]
        payload = {
            "signingType": "OTP",
            "uuid": page_query_id
        }
        s.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'
        s.headers['Accept'] = 'application/json, text/plain, */*'
        s.headers['Accept-Encoding'] = 'gzip, deflate'
        s.headers['Connection'] = 'keep-alive'
        s.headers['Content-Type'] = 'application/json'
        s.headers['Host'] = 'egov.kz'
        s.headers['Origin'] = 'https://egov.kz'
        s.headers['Referer'] = f'https://egov.kz/services/signing/?PageQueryID={page_query_id}'
        s.headers['Sec-Fetch-Mode'] = 'cors'
        s.headers['Sec-Fetch-Site'] = 'same-origin'
        # s.headers['Sec-Ch-Ua'] = 'same-origin'
        # s.headers['Sec-Ch-Ua'] = 'Google Chrome";v="117", "Not;A=Brand";v="8", "Chromium";v="117'
        # s.headers['Sec-Ch-Ua-Mobile'] = '?0'
        # s.headers['Sec-Ch-Ua-Platform'] = 'Windows'
        # s.headers['Sec-Ch-Ua-Platform'] = 'empty'
        result_code = s.options(f"https://egov.kz/services/signing/rest/app/send-otp?code={code}", data=payload)
        print(result_code)
        return Response({"status": "True"}, status=200)