from util.player_tiers_helper import get_player_id_to_player_dict

def get_position_to_player_draft_sorted_by_pick_order(league):
    """
    Creates a dictionary mapping each position to a list of player IDs, sorted by the draft pick order.
    
    Args:
    league: The fantasy football league object, containing draft information.
    
    Returns:
    A dictionary where keys are positions, and values are lists of player IDs drafted at that position, ordered by draft pick.
    """
    player_id_to_player_dict = get_player_id_to_player_dict(league)
    position_to_player_draft_pick_order = {}
    for pick_num, draft_pick in enumerate(league.draft):
        playerId = draft_pick.playerId

        if not player_id_to_player_dict.__contains__(playerId):
            continue
        player = player_id_to_player_dict[playerId]
        player_pos = player.position
        
        if not position_to_player_draft_pick_order.__contains__(player_pos):
            position_to_player_draft_pick_order[player_pos] = []
        position_to_player_draft_pick_order[player_pos].append(playerId)
    return position_to_player_draft_pick_order

def get_surrounding_players_by_position(league, target, radius, include_target = False):
    """
    Gets a list of player IDs surrounding a target player within a given radius, by draft pick order.
    Only players considered are of the same position.
    Args:
    league: The fantasy football league object.
    target: The player ID of the target player.
    radius: The number of players to include on either side of the target player.
    include_target: Whether to include the target player in the result.
    
    Returns:
    A list of player IDs surrounding the target player, ordered by draft pick.
    """
    position_to_player_draft_sorted_by_pick_order = get_position_to_player_draft_sorted_by_pick_order(league)
    player_id_to_player_dict = get_player_id_to_player_dict(league)

    target_player = player_id_to_player_dict[target]
    target_player_pos = target_player.position
    all_drafted_players_at_pos = position_to_player_draft_sorted_by_pick_order[target_player_pos]

    i = all_drafted_players_at_pos.index(target)
    if (i == -1):
        return None
    
    start_index = max(0, i - radius)
    end_index = min(len(all_drafted_players_at_pos), i + radius + 1)

    if include_target:
        considered_players = all_drafted_players_at_pos[start_index: end_index]
    else:
        considered_players = all_drafted_players_at_pos[start_index: i] + all_drafted_players_at_pos[i+1: end_index]

    return considered_players

def get_sorted_order_surrounding_drafted_players_same_position(league, target, radius, include_target=True):
    """
    Gets and sorts surrounding players by points, within a given radius, around the target player.
    
    Args:
    league: The fantasy football league object.
    target: The player ID of the target player.
    radius: The number of players to include on either side of the target player.
    include_target: Whether to include the target player in the sorting.
    
    Returns:
    A list of player IDs surrounding the target player, sorted by points.
    """
    surrounding_players = get_surrounding_players_by_position(league, target, radius, include_target)
    player_id_to_player_dict = get_player_id_to_player_dict(league)
    sorted_players = sorted(surrounding_players, key = lambda playerId: player_id_to_player_dict[playerId].stats[0]['points'], reverse=True)
    return sorted_players

def get_rank_of_player_compared_to_surrounding_drafted_players_same_position(league, target, radius):
    """
    Gets the rank of the target player compared to surrounding players by points.
    
    Args:
    league: The fantasy football league object.
    target: The player ID of the target player.
    radius: The number of players to consider around the target player.
    
    Returns:
    The rank of the target player among the surrounding players.
    """
    sorted_surrounding_players = get_sorted_order_surrounding_drafted_players_same_position(league, target, radius,include_target=True)
    rank = sorted_surrounding_players.index(target) + 1
    return rank

def get_next_drafted_players_same_position(league, target, size, include_target=True):
    """
    Gets the next set of drafted players at the same position after the target player.
    
    Args:
    league: The fantasy football league object.
    target: The player ID of the target player.
    size: The number of players to retrieve.
    include_target: Whether to include the target player in the result.
    
    Returns:
    A list of player IDs for the next drafted players at the same position.
    """
    position_to_player_draft_sorted_by_pick_order = get_position_to_player_draft_sorted_by_pick_order(league)
    player_id_to_player_dict = get_player_id_to_player_dict(league)

    target_player = player_id_to_player_dict[target]
    target_player_pos = target_player.position
    all_drafted_players_at_pos = position_to_player_draft_sorted_by_pick_order[target_player_pos]

    start_index = all_drafted_players_at_pos.index(target)
    if not include_target:
        start_index += 1

    end_index = min(len(all_drafted_players_at_pos), start_index + size)

    return all_drafted_players_at_pos[start_index: end_index]

def get_sorted_order_next_drafted_players_same_position(league, target, size, include_target=True):
    """
    Gets and sorts the next drafted players by points, at the same position as the target player.
    
    Args:
    league: The fantasy football league object.
    target: The player ID of the target player.
    size: The number of next drafted players to retrieve.
    include_target: Whether to include the target player in the sorting.
    
    Returns:
    A list of player IDs for the next drafted players, sorted by points.
    """
    next_drafted_players = get_next_drafted_players_same_position(league, target, size, include_target)
    player_id_to_player_dict = get_player_id_to_player_dict(league)
    sorted_players = sorted(next_drafted_players, key = lambda playerId: player_id_to_player_dict[playerId].stats[0]['points'], reverse=True)
    return sorted_players

def get_rank_of_player_compared_to_next_drafted_players_same_position(league, target, size):
    """
    Gets the rank of the target player compared to the next drafted players by points.
    
    Args:
    league: The fantasy football league object.
    target: The player ID of the target player.
    size: The number of next drafted players to consider.
    
    Returns:
    The rank of the target player among the next drafted players.
    """
    sorted_next_players = get_sorted_order_next_drafted_players_same_position(league, target, size, True)
    rank = sorted_next_players.index(target) + 1
    return rank