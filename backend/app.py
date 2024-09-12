from flask import Flask, jsonify, request, make_response
from flask_cors import CORS
import os
from dotenv import load_dotenv
from util.json_builder import build_advanced_stats_json

app = Flask(__name__)

# Enable CORS for all routes
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/api/getAdvancedStats', methods=['GET', 'OPTIONS'])
def get_advanced_stats():
    if request.method == "OPTIONS":
        return _build_cors_preflight_response()
    elif request.method == "GET":
        print("Received API call")

        load_dotenv()

        league_id = os.getenv('LEAGUE_ID')
        swid = os.getenv('SWID')
        espn_s2 = os.getenv('ESPN_S2')
        year = 2024
        week = 2
        league_median_name = "League Median"
        team_id_against_league_median = 6

        data = build_advanced_stats_json(league_id, swid, espn_s2, year, week, league_median_name, team_id_against_league_median)

        return _corsify_actual_response(jsonify(data))
    else:
        raise RuntimeError("Weird - don't know how to handle method {}".format(request.method))

def _build_cors_preflight_response():
    response = make_response()
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add('Access-Control-Allow-Headers', "*")
    response.headers.add('Access-Control-Allow-Methods', "*")
    return response

def _corsify_actual_response(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

if __name__ == '__main__':
    app.run(port=5000)