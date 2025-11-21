from dataclasses import dataclass
from typing import Dict


@dataclass
class Weather:
    key: str
    name: str
    intensity: int      # 1〜5
    chaos: float        # 0.0〜1.0
    reward_modifier: float
    min_required_credit: int = 0


class WeatherSystem:
    def __init__(self, config: Dict):
        self._patterns: Dict[str, Weather] = {}
        for key, weather in config["weather_patterns"].items():
            self._patterns[key] = Weather(
                key=key,
                name=weather["name"],
                intensity=weather["intensity"],
                chaos=weather["chaos"],
                reward_modifier=weather["reward_modifier"],
                min_required_credit=weather.get("min_required_credit", 0),
            )

        # デフォルトは sunny
        self._current: Weather = self._patterns.get("sunny")

    def set_weather(self, key: str) -> None:
        if key not in self._patterns:
            raise ValueError(f"Unknown weather key: {key}")
        self._current = self._patterns[key]

    @property
    def current(self) -> Weather:
        return self._current

    def can_join(self, role_credit: int) -> bool:
        """現在の天候下で、このクレジットのロールが参加してよいか判定"""
        return role_credit >= self._current.min_required_credit
