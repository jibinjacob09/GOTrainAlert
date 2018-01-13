import pycurl
from bs4 import BeautifulSoup
from io import BytesIO


class AlertPage():
    def __init__(self, url=None):
        url = "http://www.gotransit.com/publicroot/en/default.aspx" if url is None else url
        self.url = url

    def _get_raw_html(self):
        """
        uses pycurl to fetch raw html from webpage
        :return: BytesIO
        """
        buffer = BytesIO()
        c = pycurl.Curl()
        c.setopt(c.URL, self.url)
        c.setopt(c.WRITEDATA, buffer)
        c.perform()
        c.close()
        return buffer.getvalue()

    def get_all_train_alerts(self) ->dict:
        """
        parsing the raw html using beautfulsoup, and extracting all information from the alert table
        :return: all train alert information
        """
        bs = BeautifulSoup(self._get_raw_html(), "html.parser")
        alert_table = bs.find_all("tr")
        alerts_dict = dict()

        for alert in alert_table:
            _key = alert.contents[0].text.lower()

            if "delayed" in alert.contents[1].text.lower():
                lst_info = list()

                try:
                    for info in alert.contents[1].contents[1].contents[1].contents:
                        lst_info.append(info.text)
                    alerts_dict[_key] = lst_info
                except IndexError:
                    pass

            elif "on time" in alert.contents[1].text.lower():
                alerts_dict[_key] = None

        return alerts_dict

    def get_train_alert(self, service_name)->str:
        """
        filters the all_alerts dictonary and returns any delay information
        :param service_name: str; name of the train service to check
        :return: delay information
        """
        all_alerts = self.get_all_train_alerts()
        try:
            info = all_alerts[service_name.lower()]
        except KeyError:
            return "no delay informatation was found for the service name provided"

        if info is None:
            return "None"
        else:
            return ", ".join(info)
