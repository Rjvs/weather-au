import weather

# https://lxml.de/elementsoup.html

# <forecast>
#   ...
#   <area aac="VIC_PT001" description="Aireys Inlet" type="location">
#     <forecast-period index="0" start-time-local="2019-09-08T01:00:00+10:00" ...
#        <text type="uv_alert">
#          Sun protection recommended from 10:40 am to 2:00 pm, UV Index predicted to reach 4 [Moderate]

class UvAlert:

    def __init__(self, state=None):

        self.state = state
        self.soup = weather.fetch_xml(weather.UV_ALERT_PRODUCT_URL[state])
        self.identifier = self.soup.identifier.contents[0]
    

    def aac_list(self):
        # Return a dict of aac with a key of description

        aacs = {}

        for area in self.soup.find_all('area', {'type': 'location'}):
            aacs[area.attrs['description']] = area.attrs['aac']

        return aacs


    def get_aac(self, description=None):
        # Get an aac given the description

        aacs = self.aac_list()

        if description in aacs:
            return aacs[description]
        else:
            return None


    def uv_alert(self, aac=None):

        area = self.soup.find('area', {'type': 'location', 'aac': aac})

        if area is not None:
            forecast_period = area.find('forecast-period', {'index': '0'})
            #start_time = forecast_period['start-time-local']

            if forecast_period is not None:
                text = forecast_period.find('text', {'type': 'uv_alert'})

                if text is not None:
                    return text.contents[0]

        return None


    def __str__(self):
        return str(self.soup)