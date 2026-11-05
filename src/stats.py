from lichess import *

SPEED_FORMATS = {"correspondence", "classical", "rapid", "blitz", "bullet", "ultrabullet"}
DRAW_STATUSES = {"draw", "stalemate", "outoftime", "timeout"}

def get_puzzle_stats(user):
    user = user.strip().lower()
    try:
        puzzles = client.users.get_public_data(user)
        return puzzles.get("perfs", {}).get("puzzle", {}).get("rating", None), puzzles.get("perfs", {}).get("puzzle", {}).get("games", None)
        
    except requests.exceptions.ConnectionError:
        return "Connection failed"
    except requests.exceptions.Timeout:
        return "Request timed out"
    except berserk.exceptions.ResponseError:
        return "Failed to get response"
    except (KeyError, TypeError, AttributeError):
        return "Unexpected game data"

def _mode_matches(game, mode):
    """Keep mode as a string; compare against the API's rated flag."""
    if mode == "all":
        return True
    if mode == "rated":
        return game.get("rated") is True
    return game.get("rated") is False  # 'casual' and 'unrated'


def win_loss_draw_stats(user, color, format, variant, result, mode="all"):
    user = user.strip().lower()
    color = color.strip().lower()
    format = format.strip().lower()
    variant = variant.strip().lower()
    result = result.strip().lower()
    mode = mode.strip().lower()

    if color not in ("white", "black"):
        return "Choose a valid color (white or black)"
    if mode not in ("rated", "unrated", "casual", "all"):
        return "Choose a valid mode (rated, unrated, casual, or all)"
    if variant != "standard":
        return "Sorry! Only standard is available for now"
    if result not in ("win", "loss", "draw"):
        return "Choose a valid result (win, loss, or draw)"
    if format not in SPEED_FORMATS:
        return "Choose a valid speed format"

    count = 0
    try:
        games = client.games.export_by_player(user, perf_type=format)
        for game in games:
            if game.get("variant") != variant or game.get("speed") != format:
                continue
            if not _mode_matches(game, mode):
                continue

            player_id = (game.get("players", {})
                         .get(color, {})
                         .get("user", {})
                         .get("id"))
            if player_id != user:
                continue

            winner = game.get("winner")
            status = game.get("status")
            if result == "draw":
                if winner is None and status in DRAW_STATUSES:
                    count += 1
            elif result == "win":
                if winner == color:
                    count += 1
            else:  # loss
                if winner in ("white", "black") and winner != color:
                    count += 1

    except requests.exceptions.ConnectionError:
        return "Connection failed"
    except requests.exceptions.Timeout:
        return "Request timed out"
    except berserk.exceptions.ResponseError:
        return "Failed to get response"
    except (KeyError, TypeError, AttributeError):
        return "Unexpected game data"

    return count


def white_wins_count(user, format, variant, mode="all"):
    return win_loss_draw_stats(user, "white", format, variant, "win", mode)


def black_wins_count(user, format, variant, mode="all"):
    return win_loss_draw_stats(user, "black", format, variant, "win", mode)


def white_losses(user, format, variant, mode="all"):
    return win_loss_draw_stats(user, "white", format, variant, "loss", mode)


def black_losses(user, format, variant, mode="all"):
    return win_loss_draw_stats(user, "black", format, variant, "loss", mode)


def white_draws_count(user, format, variant, mode="all"):
    return win_loss_draw_stats(user, "white", format, variant, "draw", mode)


def black_draws_count(user, format, variant, mode="all"):
    return win_loss_draw_stats(user, "black", format, variant, "draw", mode)        
    


    