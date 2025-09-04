from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List


@dataclass
class PlayerFeature:
	player_id: int
	position: str
	team: str
	market_value: float | None = None


@dataclass
class Prediction:
	player_id: int
	pred_mean: float
	pred_std: float


def simple_heuristic(features: Iterable[PlayerFeature]) -> List[Prediction]:
	result: List[Prediction] = []
	for f in features:
		base = 4.0
		if f.position.upper() == "FWD":
			base = 6.0
		elif f.position.upper() == "MID":
			base = 5.0
		elif f.position.upper() == "DEF":
			base = 4.5

		# Optional market value influence (light scaling)
		if f.market_value is not None:
			try:
				mv = float(f.market_value)
				# scale down large market values; assume units are in whatever source provides
				# add a small premium up to ~+1.0 points for top valuations
				premium = min(1.0, (mv / 1_000_000.0) * 0.05)
				base += premium
			except Exception:
				pass
		# std as simple uncertainty proxy
		result.append(Prediction(player_id=f.player_id, pred_mean=base, pred_std=1.5))
	return result

