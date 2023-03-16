from dataclasses import dataclass
from player import Player

@dataclass
class Team:
    name: str
    league_position: int
    matches_played: int
    wins: int
    draws: int
    losses: int
    goals_for: int
    goals_against: int
    goal_difference: int
    xG: float
    xA: float
    players: list[Player]