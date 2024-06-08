import reverse_geocoder as rg
import math

class ReverseGeocoder:
    
    __GRID_SIZE:int = 1
    __cache:dict[tuple[int, int], dict[str, str]] = {}
    
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
    def get_grid_key(latitude, longitude):
        

        lat_to_km = 2 * math.pi * 6371.0 / 360.0
        lon_to_km = 2 * math.pi * 6371.0 * math.cos(math.radians(latitude)) / 360.0

        grid_lat = round(latitude * lat_to_km / ReverseGeocoder.__GRID_SIZE) * ReverseGeocoder.__GRID_SIZE / lat_to_km
        grid_lon = round(longitude * lon_to_km / ReverseGeocoder.__GRID_SIZE) * ReverseGeocoder.__GRID_SIZE / lon_to_km

        return (grid_lat, grid_lon)
    
    @staticmethod
    def get_location_name(latitude, longitude) -> dict:
        """
        위도와 경도를 지역 이름으로 변환
        """
        if latitude is None or longitude is None:
            return None
        
        grid_key = ReverseGeocoder.get_grid_key(latitude, longitude)
        
        if grid_key in ReverseGeocoder.__cache:
            return ReverseGeocoder.__cache[grid_key]

        result = rg.search([grid_key])
        
        city = result[0]['name']
        state = result[0]['admin1']
        country = result[0]['cc']
        location = {"city":city, "state":state, "country":country}
        ReverseGeocoder.__cache[grid_key] = location
        return location