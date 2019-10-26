import json
import os
import uuid
from urllib.parse import urlparse

from flask import Flask, jsonify, request


app = Flask(__name__)


def load_organizations():
    project_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    orgs_path = os.path.join(project_path, 'data', 'orgs')

    result = []
    for name in os.listdir(orgs_path):
        if not (name.endswith('.json') and len(name) == 32):
            continue

        with open(os.path.join(orgs_path, name)) as f:
            item = json.load(f)['result']
            result.append(item)
    return result


def normalize_domain(url):
    domain = urlparse(url).hostname
    return '.'.join(domain.split('.')[-2:])


def split_ids(value):
    return value.split(',') if value else []


organizations = load_organizations()
users = {}


@app.route('/api/autocomplete', methods=['GET'])
def autocomplete():
    query = request.args.get('query', '').lower()

    places = [item for item in organizations
              if ('name' in item and
                  query in item['name'].lower())]

    places.sort(key=lambda item: item.get('user_ratings_total', 0), reverse=True)

    known_names = set()
    known_domains = set()
    result = []
    for item in places:
        name = item['name'].lower()
        if name in known_names:
            continue
        known_names.add(name)

        if 'website' in item:
            domain = normalize_domain(item['website'])
            if domain in known_domains:
                continue
            known_domains.add(domain)
        else:
            domain = None

        result.append({
            'place_id': item['place_id'],
            'name': item['name'],
            'domain': domain,
        })

    return jsonify(result)


@app.route('/api/register', methods=['POST'])
def register():
    user_id = str(uuid.uuid4())
    liked_places = split_ids(request.form.get('liked_places'))
    disliked_places = split_ids(request.form.get('disliked_places'))

    users[user_id] = {'liked_places': liked_places,
                      'disliked_places': disliked_places}

    return jsonify({'user_id': user_id})


@app.route('/api/recommend', methods=['GET'])
def recommend():
    user_id = request.args['user_id']

    # TODO: ...

    return jsonify({})


@app.route('/api/rate', methods=['POST'])
def rate():
    user_id = request.form['user_id']
    place_id = request.form['place_id']
    liked = (request.form['liked'] == '1')

    if liked:
        users[user_id]['liked_places'].append(place_id)
    else:
        users[user_id]['disliked_places'].append(place_id)
    return ''
