def get_player_id_to_player_dict(league, free_agents_size = 100):
    free_agents = league.free_agents(size=free_agents_size)
    player_id_to_player_dict = {}
    for team in league.teams:
        roster = team.roster    
        for player in roster:
            playerId = player.playerId
            player_id_to_player_dict[playerId] = player
            
    for player in free_agents:
        playerId = player.playerId
        player_id_to_player_dict[playerId] = player
    
    return player_id_to_player_dict

def get_position_to_players_dict(league, free_agents_size = 100):
    """
    Creates a dictionary mapping each position to a list of players (both team players and free agents).

    Args:
    league: The fantasy football league object, containing teams and players.
    free_agents_size: The number of free agents to retrieve.

    Returns:
    A dictionary where the keys are player positions, and the values are lists of players for each position.
    """
    all_players_dict = get_player_id_to_player_dict(league, free_agents_size)
    position_to_players = {}

    for player in all_players_dict.values():
    
        primary_position = player.position
        if not position_to_players.__contains__(primary_position):
            position_to_players[primary_position] = []
        
        position_to_players[primary_position].append(player)
    
    return position_to_players

def get_player_id_to_tier_by_position(league, tier_size = 9, free_agents_size = 100):
    """
    Creates a dictionary mapping player IDs to their tier, based on position.

    Args:
    league: The fantasy football league object.
    tier_size: Number of players per tier.
    free_agents_size: The number of free agents to retrieve.

    Returns:
    A dictionary where keys are positions, and values are dictionaries mapping player IDs to tiers.
    """
    position_to_players = get_position_to_players_dict(league, free_agents_size)
    tier_dict_all_pos = {}
    for key in position_to_players:
        players = position_to_players[key]
        sorted_players = sorted(players, key = lambda player: player.stats[0]['points'], reverse=True)

        tier_dict_for_pos = {}

        for rank, player in enumerate(sorted_players):
            playerId = player.playerId
            
            tier_dict_for_pos[playerId] = rank // tier_size + 1

        tier_dict_all_pos[key] = tier_dict_for_pos

    return tier_dict_all_pos

def get_tier_to_players_by_team(league, tier_size = 9, free_agents_size = 100):
    """
    Creates a dictionary mapping team IDs to players organized by their tier and position.

    Args:
    league: The fantasy football league object.
    tier_size: Number of players per tier.
    free_agents_size: The number of free agents to retrieve.

    Returns:
    A dictionary where keys are team IDs, and values are dictionaries mapping position-tier pairs to lists of player IDs.
    """
    tier_dict_all_pos = get_player_id_to_tier_by_position(league, tier_size, free_agents_size)
    
    all_teams_player_to_tier_dict = {}
    for team in league.teams:
        team_id = team.team_id
        roster = team.roster  

        player_to_tier_dict = {}
        for player in roster:
            player_id = player.playerId
            player_pos = player.position
            

            player_tier = tier_dict_all_pos[player_pos][player_id]

            player_tier_key = str(player_pos) + "_" + str(player_tier)

            if not player_to_tier_dict.__contains__(player_tier_key):
                player_to_tier_dict[player_tier_key] = []
            player_to_tier_dict[player_tier_key].append(player_id)

        all_teams_player_to_tier_dict[team_id] = player_to_tier_dict

    return all_teams_player_to_tier_dict




