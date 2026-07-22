from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.database import get_session
from app.models.hero import Hero, HeroCreate, HeroPublic


router = APIRouter(prefix="/heroes", tags=["heroes"])


@router.get("", response_model=list[HeroPublic])
def read_heroes(*, session: Session = Depends(get_session), q: str | None = None):
    statement = select(Hero)
    if q:
        statement = statement.where(Hero.name == q)
    return session.exec(statement).all()


@router.post("", response_model=HeroPublic)
def create_hero(*, session: Session = Depends(get_session), hero: HeroCreate):
    db_hero = Hero.model_validate(hero)
    session.add(db_hero)
    session.commit()
    session.refresh(db_hero)
    return db_hero


@router.get("/{hero_id}", response_model=HeroPublic)
def read_hero(*, session: Session = Depends(get_session), hero_id: int):
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    return hero
