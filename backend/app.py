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

    print("Received API call")

    # Fetch query parameters with default values if not provided
    league_id = request.args.get('leagueId')
    swid = request.args.get('swid')
    espn_s2 = request.args.get('espnS2')
    year = request.args.get('year', type=int)
    week = request.args.get('week', type=int)
    league_median_name = request.args.get('leagueMedianName')
    team_id_against_league_median = request.args.get('teamIdAgainstLeagueMedian', type=int)

    # Build the advanced stats JSON
    data = build_advanced_stats_json(league_id, swid, espn_s2, year, week, league_median_name, team_id_against_league_median, tier_size=9, free_agents_size=100)

    return jsonify(data)


if __name__ == '__main__':
    app.run(port=5000)