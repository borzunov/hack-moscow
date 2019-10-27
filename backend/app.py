import json
import os
import uuid

import pandas as pd
import requests
from flask import Flask, jsonify, request

from recommender import Recommender
from utils import LatLong, lat_long_dist_in_km, normalize_place, split_ids


MAX_DIST_IN_KM = 2.0  # Hard limit on the max distance to a restaraunt

PROJECT_PATH = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
ORGS_PATH = os.path.join(PROJECT_PATH, 'data', 'orgs')
ORGS_MERGED_PATH = os.path.join(PROJECT_PATH, 'data', 'notebooks', 'orgs_merged.csv')

HERE_APP_ID = 'C9BobK4a8dRtrYCfICXn'
HERE_APP_CODE = 'EsbNtOHm6VitKrZ5DLZPow'
HERE_API_BATCH_SIZE = 200
GOOGLE_MAPS_TOKEN = os.environ["GOOGLE_MAPS_TOKEN"]
GOOGLE_PHOTO_URL = "https://maps.googleapis.com/maps/api/place/photo?maxwidth=1600&photoreference={reference}&key=" + GOOGLE_MAPS_TOKEN

SECONDS_PER_MIN = 60.0


def load_places_db():
    project_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    orgs_path = os.path.join(project_path, 'data', 'orgs')

    result = []
    for name in os.listdir(orgs_path):
        if not (name.endswith('.json') and len(name) == 32):
            continue

        with open(os.path.join(orgs_path, name)) as f:
            place = json.load(f)['result']
            place['chain_id'] = normalize_place(place)
            result.append(place)
    return result


app = Flask(__name__)

places_db = load_places_db()
users_db = {
    "5f29f9df-6c85-4dfe-822c-83b450bc043d": {
        "liked_chains": ['ChIJzX3TaKRLtUYRWXxaqlv-Mec', 'ChIJz4hlXAVLtUYRnQx4_-WcWTk', 'ChIJv6ZyGJ9LtUYRvKjPR427PjY'],
        "disliked_chains": [],
    }
}
recommender = Recommender(pd.read_csv(ORGS_MERGED_PATH))


@app.route('/api/autocomplete', methods=['GET'])
def autocomplete():
    query = request.args.get('query', '').lower()

    places = [item for item in places_db
              if ('name' in item and
                  query in item['name'].lower())]

    places.sort(key=lambda item: item.get('user_ratings_total', 0), reverse=True)

    known_chain_ids = set()
    known_names = set()
    result = []
    for item in places:
        chain_id = item['chain_id']
        name = item['name'].lower()
        if chain_id in known_chain_ids or name in known_names:
            continue
        known_chain_ids.add(chain_id)
        known_names.add(name)

        result.append({
            'chain_id': chain_id,
            'name': item['name'],
        })

    return jsonify(result)


@app.route('/api/register', methods=['POST'])
def register():
    user_id = str(uuid.uuid4())
    liked_chains = split_ids(request.form.get('liked_chains'))
    disliked_chains = split_ids(request.form.get('disliked_chains'))

    users_db[user_id] = {'liked_chains': liked_chains,
                         'disliked_chains': disliked_chains}

    return jsonify({'user_id': user_id})


def get_predictions_for(cur_user):
    places_ids = cur_user['liked_chains'] + cur_user['disliked_chains']
    ratings = [5] * len(cur_user['liked_chains']) + [1] * len(cur_user['disliked_chains'])

    n_chains = len(recommender.df.org_id.unique())
    place_rating, predictions = recommender.recommend(places_ids, ratings,
                                                      n_closest=n_chains)
    print('Top predictions now:', place_rating[:5])

    return dict(zip(place_rating, predictions))


def get_tags(place):
    # TODO: Fill tags
    return []


def get_sort_key(place, query_tags):
    n_wrong_tags = len(set(place['tags']).symmetric_difference(query_tags))
    return (n_wrong_tags, -place['prediction'], place['travel_time'])


def calc_travel_time(user_location, places):
    url = 'https://matrix.route.api.here.com/routing/7.2/calculatematrix.json'
    params = {
        'app_id': HERE_APP_ID,
        'app_code': HERE_APP_CODE,
        'mode': 'fastest;pedestrian;traffic:disabled',
        'summaryAttributes': 'traveltime',
    }
    data = {'start0': str(user_location)}
    for i, place in enumerate(places):
        place_location = LatLong.from_dict(place['geometry']['location'])
        data['destination{}'.format(i)] = str(place_location)

    response = requests.post(url, params=params, data=data)
    if not response.ok:
        print('HERE API Response:', response.status_code, response.text)

    entries = response.json()['response']['matrixEntry']

    for place, entry in zip(places, entries):
        place['travel_time'] = entry['summary']['travelTime']


@app.route('/api/recommend', methods=['GET'])
def recommend():
    user_id = request.args['user_id']
    user_location = LatLong.from_dict(request.args)
    query_tags = split_ids(request.args.get('tags'))

    cur_user = users_db[user_id]
    predictions = get_predictions_for(cur_user)

    available_places = []
    for place in places_db:
        chain_id = place['chain_id']
        if (chain_id in cur_user['liked_chains'] or
            chain_id in cur_user['disliked_chains']):
            continue

        # If there is no reviews for this chain
        if chain_id not in predictions:
            continue

        place_location = LatLong.from_dict(place['geometry']['location'])
        if lat_long_dist_in_km(user_location, place_location) > MAX_DIST_IN_KM:
            continue

        place = place.copy()
        place['tags'] = get_tags(place)
        place['prediction'] = predictions[chain_id]

        available_places.append(place)

    if not available_places:
        return jsonify({'error': 'No such places'})

    for index in range(0, len(available_places), HERE_API_BATCH_SIZE):
        places_batch = available_places[index:index + HERE_API_BATCH_SIZE]
        calc_travel_time(user_location, places_batch)

    best_place = min(available_places,
                     key=lambda item: get_sort_key(item, query_tags))

    users_db[user_id]["liked_chains"].append(best_place["chain_id"])  # hack for different places on each call

    photos = best_place["photos"]
    if len(photos) == 0:
        photo_url = None
    photo_url = GOOGLE_PHOTO_URL.format(reference=photos[0]["photo_reference"])

    return jsonify({
        'name': best_place['name'],
        'chain_id': best_place['chain_id'],
        'lat': best_place['geometry']['location']['lat'],
        'lng': best_place['geometry']['location']['lng'],
        'travel_time_mins': best_place['travel_time'] / SECONDS_PER_MIN,
        'photo_url': photo_url,
    })


@app.route('/api/rate', methods=['POST'])
def rate():
    user_id = request.form['user_id']
    chain_id = request.form['chain_id']
    liked = (request.form['liked'] == '1')

    if liked:
        users_db[user_id]['liked_chains'].append(chain_id)
    else:
        users_db[user_id]['disliked_chains'].append(chain_id)
    return ''
