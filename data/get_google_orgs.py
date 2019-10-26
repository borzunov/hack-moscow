import googlemaps
import click

import random
import json
import pathlib

gmaps = None

fields = [
    "address_component",
    "adr_address",
    "formatted_address",
    "geometry",
    "icon",
    "name",
    "permanently_closed",
    "photo",
    "place_id",
    "plus_code",
    "type",
    "url",
    "utc_offset",
    "vicinity",

    "price_level",
    "rating",
    "review",
    "user_ratings_total",

    "website",
    "opening_hours",
]


def generate_random_location(bounds):
    bottom_left_bound, top_right_bound = bounds
    min_lat, min_lon = bottom_left_bound
    max_lat, max_lon = top_right_bound
    return (
        min_lat + (max_lat - min_lat) * random.random(),
        min_lon + (max_lon - min_lon) * random.random(),
    )


def find_places(loc, radius, types=None):
    if types is None:
        types = ["cafe", "restaurant"]
    type_results = {}
    for type_ in types:
        results = []
        page = gmaps.places_nearby(location=loc, radius=radius, type=type_)
        results.extend(page["results"])
        while "next_page_token" in page:
            next_page_token = page["next_page_token"]
            try:
                page = gmaps.places_nearby(page_token=next_page_token)
            except googlemaps.exceptions.ApiError:
                continue
            results.extend(page["results"])
        type_results[type_] = results
    return type_results


@click.command()
@click.argument("bounds")
@click.argument("radius", type=int)
@click.argument("n_samples", type=int)
@click.argument("key")
@click.argument("data_path")
def collect_organizations(bounds, radius, n_samples, key, data_path="."):
    global gmaps
    bounds = list(map(float, bounds.split(",")))
    bounds = [bounds[:2], bounds[2:]]
    gmaps = googlemaps.Client(key=key)
    print(f"Will collect {n_samples} samples")
    data_path = pathlib.Path(data_path)
    places_collected = 0
    for sample_id in range(n_samples):
        loc = generate_random_location(bounds)
        results_path = data_path / f"{loc[0]}_{loc[1]}_{radius}.json"
        results = find_places(loc, radius)
        with results_path.open("w") as out:
            json.dump(results, out)
        for item in results:
            for result in results[item]:
                place_id = result["place_id"]
                place_data_file = data_path / f"{place_id}.json"
                if place_data_file.exists():
                    continue
                place_data = gmaps.place(place_id, fields=fields)
                with place_data_file.open("w") as out:
                    json.dump(place_data, out)
                    places_collected += 1
                    print(f"{sample_id + 1} samples, {places_collected} places")
        print(f"{sample_id + 1} samples, {places_collected} places")


if __name__ == '__main__':
    collect_organizations()
