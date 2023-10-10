import json
import re
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
        code = request.data.get('code')
        for cookie_name, cookie_value in cookies.items():
            s.cookies.set(cookie_name, cookie_value)
        time.sleep(3)
        s.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'
        s.headers['Host'] = 'egov.kz'
        s.get("https://egov.kz/services/P3.05/#/declaration/0//")
        res = s.get("https://egov.kz/services/P3.05/rest/current-user")
        try:
            json_data = res.json()
            iin = json_data.get('uin')
        except json.decoder.JSONDecodeError:
            print(f"Invalid JSON response received. Status Code: {res.status_code}, Content: {res.text}")
            return Response({"error": "Received invalid response from the server."}, status=500)
        print(iin)

        headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
            'Connection': 'keep-alive',
            'Content-Length': '222',
            'Content-Type': 'application/json;charset=UTF-8',
            'Host': 'egov.kz',
            'Origin': 'https://egov.kz',
            'Referer': 'https://egov.kz/services/P3.05/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
            'X-KL-kfa-Ajax-Request': 'Ajax_Request',
            'sec-ch-ua': '"Google Chrome";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': "Windows"
        }

        data = f'{{"relationship": "SELF","declarantUin": "{iin}","childUin": null,"objectTypeId": "4","documentTypeId": "002","address": "1000000000000132323","house": "12","housing": null,"apartment": null,"garage": null,"countryHouse": null}}'


        res = s.post("https://egov.kz/services/P3.05/rest/app/get-signing-url", data=data, headers=headers)
        url = res.json().get('signingUrl')
        parsed_url = urlparse(url)
        query_parameters = parse_qs(parsed_url.query)
        page_query_id = query_parameters.get("PageQueryID", [None])[0]

        res = s.get(f"https://egov.kz/services/signing/rest/app/v4/verification-types?uin={iin}&PageQueryID={page_query_id}")
        res = res.json()

        request_number = res.get('backUrl')
        print(request_number)

        headers = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
            "Connection": "keep-alive",
            "Content-Length": "2",
            "Content-Type": "application/json;charset=UTF-8",
            "Host": "egov.kz",
            "Origin": "https://egov.kz",
            "Referer": url,
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
            "X-KL-kfa-Ajax-Request": "Ajax_Request",
            "sec-ch-ua": '"Google Chrome";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "Windows"
        }
        data = '{}'
        s.post(f"https://egov.kz/services/signing/rest/otp/generate?uin={iin}", headers=headers, data=data)
        response = {
            "page_query_url": url
        }
        print('response: ', response)
        headers = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
            "Connection": "keep-alive",
            "Content-Length": "67",
            "Content-Type": "application/json",
            "Host": "egov.kz",
            "Origin": "https://egov.kz",
            "Referer": url,
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
            "X-KL-kfa-Ajax-Request": "Ajax_Request",
            "sec-ch-ua": '"Google Chrome";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "Windows"
        }

        data = f'{{"uuid": "{page_query_id}","signingType": "OTP"}}'

        s.post(f"https://egov.kz/services/signing/rest/app/send-otp?code={code}", headers=headers, data=data)
        return Response(response, status=200)


class FormaCodeView(views.APIView):
    def post(self, request):
        page_query_url = request.data.get('page_query_url')
        cookies = request.data.get('cookies')
        code = request.data.get('code')
        s = requests.Session()
        for cookie_name, cookie_value in cookies.items():
            s.cookies.set(cookie_name, cookie_value)
        s.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'
        s.headers['Host'] = 'egov.kz'
        s.get("https://egov.kz/services/P3.05/#/declaration/0//")
        s.get("https://egov.kz/services/P3.05/rest/current-user")

        headers = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
            "Connection": "keep-alive",
            "Content-Length": "67",
            "Content-Type": "application/json",
            "Host": "egov.kz",
            "Origin": "https://egov.kz",
            "Referer": page_query_url,
            "Sec-Ch-Ua": '"Google Chrome";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": '"Windows"',
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
        }
        parsed_url = urlparse(page_query_url)
        query_parameters = parse_qs(parsed_url.query)
        page_query_id = query_parameters.get("PageQueryID", [None])[0]
        data = f'{{"uuid": "{page_query_id}","signingType":"OTP"}}'
        res = s.post(f"https://egov.kz/services/signing/rest/app/send-otp?code={code}", data=data, headers=headers)
        result_url = res.json().get('backUrl')
        result_headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
            "Host": "egov.kz",
            "If-Modified-Since": "Fri, 16 Jun 2023 11:12:42 GMT",
            "If-None-Match": 'W/"3574-1686913962000"',
            "Sec-Ch-Ua": '"Google Chrome";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": '"Windows"',
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-User": "?1",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
        }
        final_result_headers = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Host": "egov.kz",
            "Referer": result_url,
            "Sec-Ch-Ua": '"Google Chrome";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": '"Windows"',
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
        }
        if res.status_code == 200:
            s.get(result_url, headers=result_headers)
            res = s.get(result_url, headers=final_result_headers)
            response = {
                "result": res.text,
                "result_url": result_url
            }
            return Response(response, 200)
        else:
            return Response({"error": "not correct code"}, 400)

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
        # s.headers["Target_URL"] = f"https://egov.kz/services/signing/rest/app/send-otp?code={code}"
        proxy_url = "http://localhost:8080"
        s.headers["Target_URL"] = f"https://egov.kz/services/P80.01/rest/current-user"
        res = s.get(proxy_url)
        print(res.text)
        result = s.get(f"https://egov.kz/services/signing/rest/app/v4/verification-types?uin=040705550178&PageQueryID={page_query_id}")
        result = result.json()
        request_number = result.get('backUrl')
        result_code = s.post(proxy_url, data=payload)
        print(result_code)
        result = s.get(f"https://egov.kz/services/P3.05/rest/request-states/{request_number}")
        return Response(result.text, status=200)

class PsychoNarcoView(views.APIView):
    def post(self, request):
        s = requests.Session()
        cookies = request.data.get('cookies')
        for cookie_name, cookie_value in cookies.items():
            s.cookies.set(cookie_name, cookie_value)
        s.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'
        s.headers['Host'] = 'egov.kz'
        s.get("https://egov.kz/services/P7.04/#/declaration/0//")
        res = s.get("https://egov.kz/services/P7.04/rest/current-user")
        iin = res.json().get('uin')
        headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
            'Connection': 'keep-alive',
            'Content-Length': '47',
            'Content-Type': 'application/json;charset=UTF-8',
            'Host': 'egov.kz',
            'Origin': 'https://egov.kz',
            'Referer': 'https://egov.kz/services/P7.04/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
            'sec-ch-ua': '"Google Chrome";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"'
        }
        print(iin)
        data = f'{{"declarantUin":"{iin}","childIin":null}}'
        res = s.post("https://egov.kz/services/P7.04/rest/app/get-signing-url", data=data, headers=headers)
        url = res.json().get('signingUrl')
        parsed_url = urlparse(url)
        query_parameters = parse_qs(parsed_url.query)
        page_query_id = query_parameters.get("PageQueryID", [None])[0]
        res = s.get(f"https://egov.kz/services/signing/rest/app/v4/verification-types?uin={iin}&PageQueryID={page_query_id}")
        res = res.json()
        request_number = res.get('backUrl')
        print(request_number)
        headers = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
            "Connection": "keep-alive",
            "Content-Length": "2",
            "Content-Type": "application/json;charset=UTF-8",
            "Host": "egov.kz",
            "Origin": "https://egov.kz",
            "Referer": url,
            "Sec-Ch-Ua": '"Google Chrome";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": '"Windows"',
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
        }
        data = '{}'
        s.post(f"https://egov.kz/services/signing/rest/otp/generate?uin={iin}", headers=headers, data=data)
        response = {
            "page_query_url": url
        }
        return Response(response, status=200)


class PsychoNarcoCodeView(views.APIView):
    def post(self, request):
        page_query_url = request.data.get('page_query_url')
        cookies = request.data.get('cookies')
        code = request.data.get('code')
        s = requests.Session()
        for cookie_name, cookie_value in cookies.items():
            s.cookies.set(cookie_name, cookie_value)
        s.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'
        s.headers['Host'] = 'egov.kz'
        s.get("https://egov.kz/services/P7.04/#/declaration/0//")
        s.get("https://egov.kz/services/P7.04/rest/current-user")

        headers = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
            "Connection": "keep-alive",
            "Content-Length": "67",
            "Content-Type": "application/json",
            "Host": "egov.kz",
            "Origin": "https://egov.kz",
            "Referer": page_query_url,
            "Sec-Ch-Ua": '"Google Chrome";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": '"Windows"',
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
        }
        parsed_url = urlparse(page_query_url)
        query_parameters = parse_qs(parsed_url.query)
        page_query_id = query_parameters.get("PageQueryID", [None])[0]
        data = f'{{"uuid": "{page_query_id}","signingType":"OTP"}}'
        res = s.post(f"https://egov.kz/services/signing/rest/app/send-otp?code={code}", data=data, headers=headers)
        result_url = res.json().get('backUrl')
        result_headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
            "Host": "egov.kz",
            "If-Modified-Since": "Fri, 16 Jun 2023 11:12:42 GMT",
            "If-None-Match": 'W/"3574-1686913962000"',
            "Sec-Ch-Ua": '"Google Chrome";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": '"Windows"',
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-User": "?1",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
        }
        final_result_headers = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Host": "egov.kz",
            "Referer": result_url,
            "Sec-Ch-Ua": '"Google Chrome";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": '"Windows"',
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
        }
        request_number = result_url.split('=')[1]
        if res.status_code == 200:
            s.get(result_url, headers=result_headers)
            print(result_url)
            res = s.get(f"https://egov.kz/services/P7.04/rest/request-states/{request_number}", headers=final_result_headers)
            response = {
                "result": res,
                "result_url": result_url
            }
            return Response(response, 200)
        else:
            return Response({"error": "not correct code"}, 400)

class PsychoNarcoStatusView(views.APIView):
    def post(self, request):
        cookies = request.data.get('cookies')
        s = requests.Session()
        result_url = request.data.get('result_url')
        request_number = result_url.split('=')[1]
        for cookie_name, cookie_value in cookies.items():
            s.cookies.set(cookie_name, cookie_value)
        final_result_headers = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Host": "egov.kz",
            "Referer": result_url,
            "Sec-Ch-Ua": '"Google Chrome";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": '"Windows"',
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
        }
        res = s.get(f"https://egov.kz/services/P7.04/rest/request-states/{request_number}", headers=final_result_headers)
        return Response(res.text, 200)