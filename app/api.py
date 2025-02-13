import requests
from flask import jsonify

token = "ProcessoSeletivoStract2025"
base_url = "https://sidebar.stract.to/api"

def get_requests(endpoint):
    header = {"Authorization": token}
    request = requests.get(f'{base_url}{endpoint}', headers=header)

    if not request.status_code == 200:
        return jsonify({"message": "Request error status code"})

    return request.json()