from urllib.parse import urlparse

import numpy as np


class LatLong:
    def __init__(self, lat, long):
        self.lat = lat
        self.long = long

    @classmethod
    def from_dict(cls, dictionary):
        return cls(float(dictionary['lat']), float(dictionary['lng']))

    def __str__(self):
        return '{:.5f},{:.5f}'.format(self.lat, self.long)


def lat_long_dist_in_km(a, b):
    """Returns approximate distance between two LatLong points in kilometers.
    Assumes that points have similar latitudes.

    See https://stackoverflow.com/a/1253545"""

    x = (a.lat - b.lat) * 110.574
    avg_lat = (a.lat + b.lat) / 2
    y = (a.long - b.long) * 111.320 * np.cos(np.deg2rad(avg_lat))
    return np.linalg.norm([x, y])


def normalize_domain(url):
    domain = urlparse(url).hostname
    return '.'.join(domain.split('.')[-2:])


DOMAIN_BLACKLIST = {
    'facebook.com', 'vk.com', 'instagram.com', 't.me',
    'ginza.ru', 'tsum.ru', 'gum.ru', '2gis.ru', 'msk.ru', 'com.ru',
}


def normalize_place(place):
    website = place.get('website')
    if website is None:
        return place['place_id']

    domain = normalize_domain(website)
    return domain if domain not in DOMAIN_BLACKLIST else website


def split_ids(value):
    return value.split(',') if value else []
