from fastapi import APIRouter, Depends, HTTPException, status
from app.dependencies import get_current_active_user
from app.models.bot import get_bot_by_id
from app.schemas.match import MatchModel
from app.schemas.user import UserModel
from app.utils.docker import run_game
from app.schemas.bot import BotModel
from typing import Annotated, Any
from app.models.match import (
    get_match_by_id,
    convert_match,
    get_bots_by_match,
    update_match,
    process_logs,
)
from app.models.tournament import (
    check_tournament_creator,
    check_tournament_access,
    get_matches_by_tournament,
)


router = APIRouter(prefix="/tournaments/{tournament_id}/matches")


@router.get(
    "/",
    response_model=list[MatchModel],
)
async def read_matches_by_tournament_id(
    current_user: Annotated[UserModel, Depends(get_current_active_user)],
    tournament_id: str,
):
    matches: list[MatchModel] | None = get_matches_by_tournament(tournament_id)

    if matches is None or not check_tournament_access(current_user, tournament_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tournament: {tournament_id} not found.",
        )

    return matches


@router.get(
    "/{match_id}",
    response_model=MatchModel,
)
async def read_match_by_id(
    current_user: Annotated[UserModel, Depends(get_current_active_user)],
    tournament_id: str,
    match_id: str,
):
    match: dict[str, Any] | None = get_match_by_id(match_id)

    if match is None or not check_tournament_access(current_user, tournament_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Match: {match_id} not found.",
        )

    return convert_match(match, detail=True)


@router.get(
    "/{match_id}/bots",
    response_model=dict[str, BotModel | None],
)
async def read_bots_by_match_id(
    current_user: Annotated[UserModel, Depends(get_current_active_user)],
    tournament_id: str,
    match_id: str,
):
    bots: dict[str, BotModel] | None = get_bots_by_match(match_id)

    if bots is None or not check_tournament_access(current_user, tournament_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Match: {match_id} not found.",
        )

    return bots


@router.put(
    "/{match_id}/run",
    response_model=dict[str, BotModel] | None,
)
async def run_match(
    current_user: Annotated[UserModel, Depends(get_current_active_user)],
    tournament_id: str,
    match_id: str,
):
    if not check_tournament_creator(current_user, tournament_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User does not have access to run this match.",
        )

    match_dict: dict[str, Any] | None = get_match_by_id(match_id)
    if match_dict is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Match: {match_id} not found.",
        )

    match: MatchModel = convert_match(match_dict, detail=True)
    if match.players is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Bots not found.",
        )

    bot_1: dict[str, Any] | None = get_bot_by_id(match.players["bot1"].id)
    bot_2: dict[str, Any] | None = get_bot_by_id(match.players["bot2"].id)
    if bot_1 is None or bot_2 is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Bots not found.",
        )

    docker_logs: dict[str, Any] | None = run_game(bot_1["code"], bot_2["code"])
    if docker_logs is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error running Docker commands",
        )

    moves, winner, loser = process_logs(match, docker_logs, bot_1, bot_2)
    if winner is None or loser is None:
        raise HTTPException(
            status_code=status.HTTP_200_OK,
            detail=f"Match: {match_id} ended in a draw.",
        )

    result: dict[str, BotModel] | None = update_match(match, winner, loser, moves)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Bots not found.",
        )

    return result
