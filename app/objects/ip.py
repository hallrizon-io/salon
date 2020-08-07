import geoip2.database
from geoip2.errors import AddressNotFoundError


class IP:
    @staticmethod
    def get_client_ip(request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    @staticmethod
    def get_location_by_ip(ip):
        location = {}
        try:
            client = geoip2.database.Reader('static/databases/GeoLite2-City.mmdb').city(ip)
            location = {
                'country': client.country.name,
                'city': client.city.name,
                'postal_code': client.postal.code,
                'location': {
                    'lat': client.location.latitude,
                    'lng': client.location.longitude
                }
            }
        except AddressNotFoundError:
            pass
        return location
