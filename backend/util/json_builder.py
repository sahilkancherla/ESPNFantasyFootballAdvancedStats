from espn_api.football import League
from util.league_median_helper import get_current_and_projected_scores_for_week, get_league_median_not_including_league_median_opponent
from util.player_tiers_helper import get_tier_to_players_by_team

def build_advanced_stats_json(league_id, swid, espn_s2, current_year, current_week, league_median_name, team_id_against_league_median, tier_size, free_agents_size):

    message = {}

    league = League(league_id=league_id, year=current_year, espn_s2=espn_s2, swid=swid)

    # get initial league information
    #  - league name, league style
    #  - get team_id, team_name, primary owner name
    
    message["leagueData"] = get_league_information(league)

    # get players
    #  - map id to player information

    # get advanced stats

    message["currentWeekScoresData"] = get_current_data(league, current_week, league_median_name)

    # get league median data
    
    message["leagueMedianData"] = get_league_median_information(league, current_week=current_week, league_median_name=league_median_name, team_id_against_league_median = team_id_against_league_median)
    
    # get player tier info depending on current roster

    message["playerTierInformation"] = get_player_tier_information(league, tier_size, free_agents_size)

    return message

    
def get_league_information(league):
    league_information = {}

    league_information["league_id"] = league.league_id
    league_information["year"] = league.year

    teams = {}
    members = {}
    for team in league.teams:
        team_dict = {}
    
        team_id = team.team_id
        team_dict['teamName'] = team.team_name
        
        member_dict = {}
        owner = team.owners[0] # take just primary owner
        member_id_raw = owner['id']
        member_id = member_id_raw[1:len(member_id_raw)-1] # get rid of { and }
        member_dict["firstName"] = owner['firstName'].lower()
        member_dict["lastName"] = owner['lastName'].lower()
        member_dict["teamId"] = team_id

        team_dict['ownerId'] = member_id
        
        teams[team_id] = team_dict
        members[member_id] = member_dict
            
    league_information["teams"] = teams
    league_information["members"] = members
    
    return league_information

def get_current_data(league, current_week, league_median_name):
    teams_and_current_scores, teams_and_projected_scores = get_current_and_projected_scores_for_week(league, current_week, league_median_name)
    
    week_data = {}
    current_week_scores = {}
    projected_week_scores = {}

    for team_id, current_score in teams_and_current_scores:
        current_week_scores[team_id] = current_score

    for team_id, projected_score in teams_and_projected_scores:
        projected_week_scores[team_id] = projected_score

    week_data["currentScores"] = current_week_scores
    week_data["projectedScores"] = projected_week_scores

    return week_data

def get_league_median_information(league, current_week, league_median_name, team_id_against_league_median):

    current_median, projected_median, below_league_median_team_id, above_league_median_team_id = get_league_median_not_including_league_median_opponent(league, current_week, league_median_name, team_id_against_league_median)

    league_median_information = {}

    league_median_information["currentMedian"] = current_median
    league_median_information["projectedMedian"] = projected_median
    league_median_information["belowLeagueMedianTeamId"] = below_league_median_team_id
    league_median_information["aboveLeagueMedianTeamId"] = above_league_median_team_id
    league_median_information["teamIdAgainstLeagueMedian"] = team_id_against_league_median

    return league_median_information

def get_player_tier_information(league, tier_size, free_agents_size = 100):
    
    tiers_to_players = get_tier_to_players_by_team(league, tier_size, free_agents_size)
    
    return tiers_to_players