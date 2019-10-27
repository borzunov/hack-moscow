import json
import os
import uuid

import pandas as pd
from flask import Flask, jsonify, request

from recommender import Recommender
from utils import LatLong, lat_long_dist_in_km, normalize_place, split_ids


app = Flask(__name__)


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


PROJECT_PATH = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
ORGS_PATH = os.path.join(PROJECT_PATH, 'data', 'orgs')
ORGS_MERGED_PATH = os.path.join(PROJECT_PATH, 'data', 'notebooks', 'orgs_merged.csv')


places_db = load_places_db()
users_db = {}
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


MAX_DIST_IN_KM = 4.0  # Hard limit on the maximum distance


@app.route('/api/recommend', methods=['GET'])
def recommend():
    user_id = request.args['user_id']
    user_location = LatLong(float(request.args['lat']), float(request.args['lng']))
    query_tags = split_ids(request.args.get('tags'))

    cur_user = users_db[user_id]
    predictions = get_predictions_for(cur_user)

    available_places = []
    for place in places_db:
        chain_id = place['chain_id']
        if (chain_id in cur_user['liked_chains'] or
            chain_id in cur_user['disliked_chains'] or
            chain_id not in predictions):
            continue

        place_location = place['geometry']['location']
        place_location = LatLong(place_location['lat'], place_location['lng'])
        if lat_long_dist_in_km(user_location, place_location) > MAX_DIST_IN_KM:
            continue

        place = place.copy()
        place['tags'] = get_tags(place)
        place['prediction'] = predictions[chain_id]

        # TODO: Calc and consider travelTime using HERE API
        place['travel_time'] = 1.0

        available_places.append(place)

    if not available_places:
        return jsonify({'error': 'No such places'})

    best_place = min(available_places,
                     key=lambda item: get_sort_key(item, query_tags))
    return jsonify({
        'name': best_place['name'],
        'chain_id': best_place['chain_id'],
        'lat': best_place['geometry']['location']['lat'],
        'lng': best_place['geometry']['location']['lng'],
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
