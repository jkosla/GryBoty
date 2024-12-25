from fastapi import APIRouter, Depends, HTTPException, status
from app.dependencies import get_current_active_user
from app.schemas.tournament import TournamentModel
from app.schemas.user import UserModel
from app.schemas.bot import BotModel
from typing import Annotated
from app.models.tournament import (
    check_tournament_access,
    get_tournament_by_id,
    convert_tournament,
    get_bots_by_tournament,
    get_own_tournaments,
)


router = APIRouter(prefix="/tournaments")


@router.get("/", response_model=list[TournamentModel])
async def read_own_tournaments(
    current_user: Annotated[UserModel, Depends(get_current_active_user)],
):
    return get_own_tournaments(current_user)


@router.get("/{tournament_id}", response_model=TournamentModel)
async def read_tournament_by_id(
    current_user: Annotated[UserModel, Depends(get_current_active_user)],
    tournament_id: str,
):
    if not check_tournament_access(current_user, tournament_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tournament: {tournament_id} not found.",
        )

    return convert_tournament(get_tournament_by_id(tournament_id), detail=True)


@router.get(
    "/{tournament_id}/bots",
    response_model=list[BotModel],
)
async def read_bots_by_tournament_id(
    current_user: Annotated[UserModel, Depends(get_current_active_user)],
    tournament_id: str,
):
    if not check_tournament_access(current_user, tournament_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tournament: {tournament_id} not found.",
        )

    return get_bots_by_tournament(tournament_id)
