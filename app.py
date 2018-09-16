import json
import requests
from flask import Flask, jsonify, request

app = Flask(__name__)


def prepare_data(data):
    res = {
        'title': data['title'][0],
        'labels': [data['labels'][0]],
        'body': data['body'][0]
    }
    owner = data['owner'][0]
    repo = data['repo'][0]
    auth = data['auth'][0]
    return res, owner, repo, auth


def generate_url(owner, repo):
    url = "https://api.github.com/repos/{owner}/{repo}/issues".format(
        owner=owner, repo=repo)
    return url


def github_request(url, data, headers):
    r = requests.post(url, data=data, headers=headers)
    if r.status_code != 201:
        return {'error': 'request error'}, r.status_code
    return r.text, r.status_code


@app.route('/issues', methods=['GET'])
def request_github():
    data = dict(request.args)
    data, owner, repo, auth = prepare_data(data)
    url = generate_url(owner, repo)
    headers = {'Content-Type': 'application/json',
               'Authorization': 'Basic {}'.format(auth)}
    res, status_code = github_request(url, json.dumps(data), headers=headers)
    return jsonify({'result': res, 'status_code': status_code})


if __name__ == '__main__':
    app.run(debug=True)
