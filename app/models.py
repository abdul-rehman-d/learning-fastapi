from sqlmodel import Field, Relationship, SQLModel


class TeamBase(SQLModel):
    name: str = Field(index=True)
    headquarters: str


class HeroBase(SQLModel):
    name: str = Field(index=True)
    secret_name: str
    age: int | None = Field(default=None, index=True)

    team_id: int | None = Field(default=None, foreign_key="team.id")


class Team(TeamBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

    heroes: list["Hero"] = Relationship(back_populates="team")


class Hero(HeroBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

    team: Team | None = Relationship(back_populates="heroes")


class TeamUpdate(SQLModel):
    name: str | None = None
    headquarters: str | None = None


class HeroUpdate(SQLModel):
    name: str | None = None
    secret_name: str | None = None
    age: int | None = None
    team_id: int | None = None


class TeamCreate(TeamBase):
    pass


class HeroCreate(HeroBase):
    pass


class TeamPublic(TeamBase):
    id: int


class HeroPublic(HeroBase):
    id: int


class TeamPublicWithHeroes(TeamPublic):
    heroes: list["HeroPublic"] = []


class HeroPublicWithTeam(HeroPublic):
    team: TeamPublic | None = None
