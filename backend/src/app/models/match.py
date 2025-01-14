from fastapi import HTTPException, status
from bson import ObjectId
from typing import Any

from app.models.bot import get_bot_by_id, convert_bot
from database.main import MongoDB, Bot, Match
from app.schemas.match import MatchModel
from app.schemas.bot import BotModel


def get_match_by_id(db: MongoDB, match_id: ObjectId) -> dict[str, Any]:
    """
    Retrieves a match from the database by its ID.
    Raises an error if the match does not exist.
    """

    matches_collection = Match(db)
    match = matches_collection.get_match_by_id(match_id)

    if match is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Match: {match_id} not found.",
        )

    return match


def convert_match(
    db: MongoDB, match_dict: dict[str, Any], detail: bool = False
) -> MatchModel:
    """
    Converts a dictionary to a MatchModel object.
    """

    players = match_dict.pop("players")
    winner_id = match_dict.pop("winner")
    if not detail:
        match_dict.pop("moves")
        return MatchModel(**match_dict)

    match_dict["players"] = {}
    for key, bot_id in players.items():
        bot = get_bot_by_id(db, bot_id)
        match_dict["players"][key] = convert_bot(db, bot)

    if winner_id is not None:
        winner = get_bot_by_id(db, winner_id)
        match_dict["winner"] = convert_bot(db, winner)

    return MatchModel(**match_dict)


def get_bots_by_match_id(db: MongoDB, match_id: ObjectId) -> dict[str, BotModel]:
    """
    Retrieves all bots from the database that participate in a specific match.
    """

    match_dict = get_match_by_id(db, match_id)
    match = convert_match(db, match_dict, detail=True)

    if match.players is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No bots not found for match: {match_id}.",
        )

    return match.players


def update_match(
    db: MongoDB,
    match: MatchModel,
    winner: BotModel,
    loser: BotModel,
    moves: list[str],
) -> dict[str, BotModel]:
    """
    Updates the database with the results of a match.
    Returns the winner and loser bots with updated stats.
    Returns None if the bots do not exist.
    """

    matches_collection = Match(db)
    matches_collection.set_winner(ObjectId(match.id), ObjectId(winner.id))
    for move in moves:
        matches_collection.add_move(ObjectId(match.id), move)

    bots_collection = Bot(db)
    bots_collection.update_stats(ObjectId(winner.id), won=True)
    bots_collection.update_stats(ObjectId(loser.id), won=False)

    winner_dict = get_bot_by_id(db, winner.id)
    loser_dict = get_bot_by_id(db, loser.id)

    return {
        "winner": convert_bot(db, winner_dict),
        "loser": convert_bot(db, loser_dict),
    }


def process_logs(
    logs: dict[str, Any],
    bot_1: BotModel,
    bot_2: BotModel,
) -> tuple[list[str], BotModel, BotModel] | tuple[list[str], None, None]:
    """
    Processes the logs from a match and returns the moves, the winner and loser bots.
    Returns None if the match ended in a draw.
    """

    moves: list[str] = logs["states"]
    winner: int | None = logs["winner"]

    if winner == 0:
        return moves, bot_1, bot_2
    elif winner == 1:
        return moves, bot_2, bot_1

    return moves, None, None
