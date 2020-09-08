import requests
import re
import json
import sys
from bs4 import BeautifulSoup


class PennsylvaniaScrapper:
    """
    The class containing all the methods for
    fetching the required data
    """

    def __init__(self, url, fname, lname, dob):
        self.url = url
        self.fname = fname
        self.lname = lname
        self.dob = dob
        self.headers = {'Content-Type': 'application/x-www-form-urlencoded',
                        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
                        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Safari/537.36'}

    def get_cookies(self):
        # the method is getting the cookies
        response = requests.get(self.url, headers=self.headers, verify=False)
        self.cookies = response.cookies
        return response

    @staticmethod
    def form_data1(event_target, view_state, scroll_pos_x, scroll_pos_y, captcha):
        # contents required for the first post request form
        return {
            "__EVENTTARGET": event_target,
            "__EVENTARGUMENT": '',
            "__LASTFOCUS": '',
            "__VIEWSTATE": view_state,
            "__VIEWSTATEGENERATOR": "4AB257F3",
            "__SCROLLPOSITIONX": scroll_pos_x,
            "__SCROLLPOSITIONY": scroll_pos_y,
            "ctl00$ctl00$ctl00$cphMain$cphDynamicContent$ddlSearchType": "ParticipantName",
            "ctl00$ctl00$ctl00$ctl07$captchaAnswer": captcha
        }

    def set_form_data1(self, response):
        # getting the required data in the form_data1 with the help of beautifulsoup
        soup = BeautifulSoup(response.content, "html.parser")
        event_target = "ctl00$ctl00$ctl00$cphMain$cphDynamicContent$ddlSearchType"
        view_state = soup.find('input', {'name': '__VIEWSTATE'}).attrs['value']
        scroll_pos_x = soup.find(
            'input', {'name': '__SCROLLPOSITIONX'}).attrs['value']
        scroll_pos_y = soup.find(
            'input', {'name': '__SCROLLPOSITIONY'}).attrs['value']

        return self.form_data1(event_target, view_state,
                               scroll_pos_x, scroll_pos_y, self.get_captcha(soup))

    def post_request1(self, data):
        # first post request and posting the data required for the first page
        return requests.post(self.url, headers=self.headers,
                             cookies=self.cookies, data=data, verify=False)

    @staticmethod
    def form_data2(view_state, scroll_pos_x, scroll_pos_y, captcha, fname, lname, dob):
        # contents required for the second post request form
        return {
            "__EVENTTARGET": '',
            "__EVENTARGUMENT": '',
            "__LASTFOCUS": '',
            "__VIEWSTATE": view_state,
            "__VIEWSTATEGENERATOR": "4AB257F3",
            "__SCROLLPOSITIONX": scroll_pos_x,
            "__SCROLLPOSITIONY": scroll_pos_y,
            "ctl00$ctl00$ctl00$cphMain$cphDynamicContent$ddlSearchType": "ParticipantName",
            "ctl00$ctl00$ctl00$cphMain$cphDynamicContent$cphSearchControls$udsParticipantName$txtLastName": lname,
            "ctl00$ctl00$ctl00$cphMain$cphDynamicContent$cphSearchControls$udsParticipantName$txtFirstName": fname,
            "ctl00$ctl00$ctl00$cphMain$cphDynamicContent$cphSearchControls$udsParticipantName$dpDOB$DateTextBox": dob,
            "ctl00$ctl00$ctl00$cphMain$cphDynamicContent$cphSearchControls$udsParticipantName$ddlDocketType": "CR",
            "ctl00$ctl00$ctl00$cphMain$cphDynamicContent$btnSearch": "Search",
            "ctl00$ctl00$ctl00$ctl07$captchaAnswer": captcha
        }

    def set_form_data2(self, response):

        soup = BeautifulSoup(response.content, "html.parser")
        view_state = soup.find('input', {'name': '__VIEWSTATE'}).attrs['value']
        scroll_pos_x = soup.find(
            'input', {'name': '__SCROLLPOSITIONX'}).attrs['value']
        scroll_pos_y = soup.find(
            'input', {'name': '__SCROLLPOSITIONY'}).attrs['value']

        return self.form_data2(view_state, scroll_pos_x,
                               scroll_pos_y, self.get_captcha(soup), self.fname, self.lname, self.dob)

    def post_request2(self, data):
        # second post request and posting the data required for the second form page
        return requests.post(self.url, headers=self.headers,
                             cookies=self.cookies, data=data, verify=False)

    def get_output(self, response):
        # the method will get the data in the reqiured format
        soup = BeautifulSoup(response.content, "html.parser")
        records = list()
        cards = soup.find_all('tr', {'class': 'gridViewRow'})
        if cards:
            for card in cards:
                try:
                    table_data = card.find_all("td")
                    if table_data:
                        record = {
                            "docket_number": table_data[7].text.strip(),
                            "court_office": table_data[8].text.strip(),
                            "short_caption": table_data[9].text.strip(),
                            "filling_date": table_data[10].text.strip(),
                            "country": table_data[11].text.strip(),
                            "case_status": table_data[12].text.strip(),
                            "primary_participant": table_data[13].text.strip(),
                            "OTN": table_data[15].text.strip(),
                            "complaint_number": table_data[18].text.strip(),
                            "police_incident": table_data[18].text.strip(),
                            "date_of_birth": table_data[19].text.strip()
                        }
                        records.append(record)
                except ValueError:
                    print("the table contents changed")
            return records

    def scrap(self):
        """
        A single interface for calling the methods in the class
        the required data is being set and used by the differtent methods
        for performing the the task and fecthing the data 
        """
        try:          
            resp1 = self.get_cookies()
            data = self.set_form_data1(resp1)

            resp2 = self.post_request1(data)
            data = self.set_form_data2(resp2)

            resp3 = self.post_request2(data)
            return scrapper.get_output(resp3)
        except:
            print("got error in scrap function")

    @staticmethod
    def get_captcha(soup):
        # captacha solving method
        all_scripts = soup.find_all('script', {'type': 'text/javascript'})
        keyValueMatch = re.findall("value = '.*;", str(all_scripts))[0]
        return re.findall("-*[0-9]+", keyValueMatch)[0]


if __name__ == "__main__":
    """
    class object 
    # passing the arguments in the format (url , fitstname,lastname,date)

    """
    scrapper = PennsylvaniaScrapper(
        'https://ujsportal.pacourts.us/DocketSheets/MDJ.aspx',  'william', 'rios', '07/31/1975'
    )

    data = scrapper.scrap()
    json_data = json.dumps(data)
    print(json_data)
