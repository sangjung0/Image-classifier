import reverse_geocoder as rg

class ReverseGeocoder:
    @staticmethod
    def convert_gps_data(value, ref:str):
        if value is None or ref is None:
            return None

        degrees = value[0]
        minutes = value[1]
        seconds = value[2]

        decimal_degrees = degrees + (minutes / 60.0) + (seconds / 3600.0)
        if ref in ['S', 'W']:
            decimal_degrees = -decimal_degrees

        return decimal_degrees
    
    @staticmethod
    def get_location_name(latitude, longitude) -> dict:
        """
        위도와 경도를 지역 이름으로 변환
        """
        if latitude is None or longitude is None:
            return None

        coordinates = (latitude, longitude)
        result = rg.search(coordinates)
        city = result[0]['name']
        state = result[0]['admin1']
        country = result[0]['cc']
        return {city, state, country}