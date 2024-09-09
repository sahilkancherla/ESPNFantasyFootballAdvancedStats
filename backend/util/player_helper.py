def get_valid_position_slots(league):
    """
    Get the valid position slots for a league.

    Args:
        league (League): ESPN Fantasy League object.

    Returns:
        list: A single list containing all the valid slots in the league.

    Example:
        >>> league = League(...)  # Initialize your League object
        >>> get_valid_position_slots(league)
        ['QB', 'RB', 'WR', 'RB/WR/TE', ...]
    """
    settings = league.settings
    position_slot_counts = settings.position_slot_counts
    valid_slots = []
    for possible_slot in position_slot_counts:
        if position_slot_counts[possible_slot] > 0:
            valid_slots.append(possible_slot)
    return valid_slots

def get_valid_position_slots_and_count(league, delimeter = '/', ignore_slots = []):

    """
    Get the valid position slots and the associated count for each slot for a league.

    Args:
        league (League): ESPN Fantasy League object.

    Returns:
        dict: A dictionary containing all the valid position slots in the league and
              their associated count. The keys are position slots (e.g., "QB", "RB"), 
              and the values are the number of slots available for each position.

    Example:
        >>> league = League(...)  # Initialize your League object
        >>> get_valid_position_slots(league)
        {'QB': 2, 'RB': 4, 'WR': 3, 'TE': 2, 'K': 1, 'DST': 1}
    """

    valid_position_slots = get_valid_position_slots(league)
    sorted_valid_position_slots = sorted(valid_position_slots, key=lambda slot: slot.count(delimeter))
    position_slot_counts = league.settings.position_slot_counts
    slot_to_count = {}
    for slot in sorted_valid_position_slots:
        if position_slot_counts[slot] > 0 and not ignore_slots.__contains__(slot):
            slot_to_count[slot] = position_slot_counts[slot]

    return slot_to_count

def get_team_actual_lineup_given_week(league, team_name, week, ignore_slots = ["BE", "IR"]):
    """
    Get the roster of a specific team for a given week.

    Args:
        league (League): ESPN Fantasy League object.
        team_name (str): Name of the team to retrieve.
        week (int): The week number to get the lineup for.

    Returns:
        dict: A dictionary where the keys are each position in the fantasy roster, and 
              the values are the players at those positions. Returns None if no team is found.
              Includes all slots found in the lineup of that week's box score.

    Example:
        >>> league = League(...)  # Initialize your League object
        >>> get_team_actual_lineup_given_week(league, "Rigged AF", 1)
        {'QB': [Player1, Player2], 'RB': [Player3, Player4, Player5, Player6], ...}
    """
    for box_score in league.box_scores(week = week):
        if box_score.home_team.team_name == team_name:
            lineup = box_score.home_lineup
        elif box_score.away_team.team_name == team_name:
            lineup = box_score.away_lineup
        else:
            continue

        starting_lineup_dict = {}

        for player in lineup:

            lineup_slot = player.lineupSlot
            if not ignore_slots.__contains__(lineup_slot):
                if not starting_lineup_dict.__contains__(lineup_slot):
                    starting_lineup_dict[lineup_slot] = []
                starting_lineup_dict[lineup_slot].append(player)
            
        return starting_lineup_dict
    
    return None

def get_team_actual_lineup_player_ids_given_week(league, team_name, week, ignore_slots = ["BE", "IR"]):
    """
    Get the roster of a specific team for a given week.

    Args:
        league (League): ESPN Fantasy League object.
        team_name (str): Name of the team to retrieve.
        week (int): The week number to get the lineup for.

    Returns:
        dict: A dictionary where the keys are each position in the fantasy roster, and 
              the values are the ids of the players at those positions. Returns None if no team is found.
              Includes all slots found in the lineup of that week's box score.

    Example:
        >>> league = League(...)  # Initialize your League object
        >>> get_team_actual_lineup_given_week(league, "Rigged AF", 1)
        {'QB': [Player1Id, Player2Id], 'RB': [Player3Id, Player4Id, Player5Id, Player6Id], ...}
    """
    for box_score in league.box_scores(week = week):
        if box_score.home_team.team_name == team_name:
            lineup = box_score.home_lineup
        elif box_score.away_team.team_name == team_name:
            lineup = box_score.away_lineup
        else:
            continue

        starting_lineup_dict = {}

        for player in lineup:

            lineup_slot = player.lineupSlot
            if not ignore_slots.__contains__(lineup_slot):
                if not starting_lineup_dict.__contains__(lineup_slot):
                    starting_lineup_dict[lineup_slot] = []
                starting_lineup_dict[lineup_slot].append(player.playerId)
            
        return starting_lineup_dict
    
    return None


def get_team_actual_lineup_given_week_total_points(league, team_name, week, ignore_slots = ["BE", "IR"]):
    """
    Calculate the total points for a specific team for a given week, excluding certain positions.

    Args:
        league (League): ESPN Fantasy League object.
        team_name (str): Name of the team to calculate points for.
        week (int): The week number to get the points for.
        ignore_slots (list): List of slots to ignore when calculating total points (default is ["BE", "IR"]).

    Returns:
        int: Total points scored by the team for the given week. Returns None if no team is found.

    Example:
        >>> league = League(...)  # Initialize your League object
        >>> get_team_actual_lineup_given_week_total_points(league, "Rigged AF", 1)
        150
    """
    team_lineup_dict = get_team_actual_lineup_given_week(league, team_name, week, ignore_slots = ignore_slots)

    if team_lineup_dict == None:
        return None
    
    total_points = 0.0

    for position in team_lineup_dict:

        if not ignore_slots.__contains__(position):
            total_points += get_total_points_given_players(team_lineup_dict[position])

    return total_points

def get_total_points_given_players(players):
    """
    Calculate the total points for a list of players.

    Args:
        players (list): A list of player objects.

    Returns:
        int: Total points scored by the list of players.

    Example:
        >>> players = [Player1, Player2, Player3]
        >>> get_total_points_given_players(players)
        45
    """
    total_points = 0.0

    for player in players:
        total_points += get_player_points_or_projected_points(player)

    return round(total_points, 2)
    

def get_player_eligible_slots_given_week(league, team_name, week):
    """
    Get the eligible position slots for each player on a team for a given week.

    Args:
        league (League): ESPN Fantasy League object.
        team_name (str): Name of the team to retrieve eligible slots for.
        week (int): The week number to get the eligible slots for.

    Returns:
        dict: A dictionary where the keys are eligible slots and the values are lists of players
              who are eligible for those slots. Returns None if no team is found.

    Example:
        >>> league = League(...)  # Initialize your League object
        >>> get_player_eligible_slots_given_week(league, "Rigged AF", 1)
        {'QB': [Player1], 'RB': [Player2, Player3], 'WR': [Player4, Player5], ...}
    """
    for box_score in league.box_scores(week = week):
        if box_score.home_team.team_name == team_name:
            lineup = box_score.home_lineup
        elif box_score.away_team.team_name == team_name:
            lineup = box_score.away_lineup
        else:
            continue

        player_eligible_slots = {}
        valid_slots = get_valid_position_slots(league)

        for player in lineup:
            
            eligible_slots = player.eligibleSlots

            for eligible_slot in eligible_slots:
                if valid_slots.__contains__(eligible_slot):
                    if not player_eligible_slots.__contains__(eligible_slot):
                        player_eligible_slots[eligible_slot] = []
                    player_eligible_slots[eligible_slot].append(player)
        
        return player_eligible_slots
    
    return None

def get_player_points_or_projected_points(player):
    """
    Get the points for a player, considering if the game has been played.

    Args:
        player (Player): The player object to get points for.

    Returns:
        float: The player's points if the game is played, otherwise the projected points.

    Example:
        >>> player = Player(...)  # Initialize your Player object
        >>> get_player_points_or_projected_points(player)
        12.5
    """
    if player.game_played < 100:
        return player.projected_points
    return player.points

def get_player_with_most_points_actual_or_projected(players):
    """
    Find the player with the most points, considering both actual and projected points.

    Args:
        players (list): A list of player objects.

    Returns:
        Player: The player with the highest points or projected points.

    Example:
        >>> players = [Player1, Player2, Player3]
        >>> get_player_with_most_points_actual_or_projected(players)
        Player2
    """
    max_points_player = None
    max_points = 0.0
    for player in players:

        if max_points_player is None:
            max_points_player = player
            max_points = get_player_points_or_projected_points(player)
        else:
            current_player_points = get_player_points_or_projected_points(player)

            if current_player_points > max_points:
                max_points = current_player_points
                max_points_player = player
    return max_points_player

def get_team_best_lineup_given_week(league, team_name, week, ignore_slots = ["BE", "IR"]):
    """
    Get the best lineup for a team for a given week by maximizing points.

    Args:
        league (League): ESPN Fantasy League object.
        team_name (str): Name of the team to optimize the lineup for.
        week (int): The week number to get the best lineup for.
        ignore_slots (list): List of slots to ignore when optimizing the lineup (default is ["BE", "IR"]).

    Returns:
        dict: A dictionary where the keys are positions and the values are lists of the best players 
              for those positions.

    Example:
        >>> league = League(...)  # Initialize your League object
        >>> get_team_best_lineup_given_week(league, "Rigged AF", 1)
        {'QB': [BestQBPlayer], 'RB': [BestRBPlayer1, BestRBPlayer2], ...}
    """
    position_to_count = get_valid_position_slots_and_count(league, ignore_slots = ignore_slots)
    eligible_slots = get_player_eligible_slots_given_week(league, team_name, week)

    best_team = {}

    for position in position_to_count:

        count_to_fill_position = position_to_count[position]
        players_for_position = []
        players_available = eligible_slots[position]

        for i in range(count_to_fill_position):

            # get player with max points
            max_points_player = get_player_with_most_points_actual_or_projected(players_available)
            players_for_position.append(max_points_player)

            # remove that player from all lists
            for slot in eligible_slots:
                if eligible_slots[slot].__contains__(max_points_player):
                    eligible_slots[slot].remove(max_points_player)

        best_team[position] = players_for_position
    
    return best_team

def get_team_best_lineup_player_ids_given_week(league, team_name, week, ignore_slots = ["BE", "IR"]):
    """
    Get the best lineup for a team for a given week by maximizing points.

    Args:
        league (League): ESPN Fantasy League object.
        team_name (str): Name of the team to optimize the lineup for.
        week (int): The week number to get the best lineup for.
        ignore_slots (list): List of slots to ignore when optimizing the lineup (default is ["BE", "IR"]).

    Returns:
        dict: A dictionary where the keys are positions and the values are lists of the ids of the best players 
              for those positions.

    Example:
        >>> league = League(...)  # Initialize your League object
        >>> get_team_best_lineup_given_week(league, "Rigged AF", 1)
        {'QB': [BestQBPlayerId], 'RB': [BestRBPlayer1Id, BestRBPlayer2Id], ...}
    """
    position_to_count = get_valid_position_slots_and_count(league, ignore_slots = ignore_slots)
    eligible_slots = get_player_eligible_slots_given_week(league, team_name, week)

    best_team = {}

    for position in position_to_count:

        count_to_fill_position = position_to_count[position]
        players_for_position = []
        players_available = eligible_slots[position]

        for i in range(count_to_fill_position):

            # get player with max points
            max_points_player = get_player_with_most_points_actual_or_projected(players_available)
            players_for_position.append(max_points_player.playerId)

            # remove that player from all lists
            for slot in eligible_slots:
                if eligible_slots[slot].__contains__(max_points_player):
                    eligible_slots[slot].remove(max_points_player)

        best_team[position] = players_for_position
    
    return best_team

def get_team_best_lineup_given_week_total_points(league, team_name, week, ignore_slots = ["BE", "IR"]):
    """
    Calculate the total points for the best lineup of a team for a given week.

    Args:
        league (League): ESPN Fantasy League object.
        team_name (str): Name of the team to get the best lineup for.
        week (int): The week number to calculate the total points for.
        ignore_slots (list): List of slots to ignore when calculating total points (default is ["BE", "IR"]).

    Returns:
        int: Total points of the best possible lineup for the team. Returns None if no team is found.

    Example:
        >>> league = League(...)  # Initialize your League object
        >>> get_team_best_lineup_given_week_total_points(league, "Rigged AF", 1)
        150
    """
    best_team = get_team_best_lineup_given_week(league, team_name, week, ignore_slots = ignore_slots)

    starters = []
    for position_starters in best_team.values():
        for position_starter in position_starters:
            starters.append(position_starter)
    
    return get_total_points_given_players(starters)
