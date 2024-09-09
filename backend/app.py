from flask import Flask, jsonify, request
import requests
from dotenv import load_dotenv
import os
from util.json_builder import build_advanced_stats_json

app = Flask(__name__)

# primary route that gets all the data
@app.route('/api/getAdvancedStats', methods=['GET'])
def your_data():

    load_dotenv()

    league_id = os.getenv('LEAGUE_ID')
    swid = os.getenv('SWID')
    espn_s2 = os.getenv('ESPN_S2')
    year = 2024
    week = 1

    data = build_advanced_stats_json(league_id, swid, espn_s2, year, week)

    return jsonify(data)

if __name__ == '__main__':
    app.run(port=5000)  # Make sure this port is consistent with your frontend's API_URL