import itertools
from datetime import datetime, date
from typing import Iterable, Dict, List, Tuple

from parsoda.model import Reducer
from parsoda.utils.roi import RoI


class ReduceByTrajectories(
    Reducer[
            str,                                    # K
            Tuple[datetime, RoI],                   # V
            Dict[date, List[Tuple[datetime, RoI]]]  # R
        ]
):

    def __init__(self, min_trajectory_length: int = 1):
        self.min_trajectory_length = min_trajectory_length

    def reduce(self, key: str, values: List[Tuple[datetime, RoI]]) -> Dict[date, List[RoI]]:
        # print(f"[ReduceByTrajectories] {key}:{len(values)}")
        
        # values.sort(key=lambda x: x[0])  # sorts respect to datetime
        day_trajectories: Dict[date, List[RoI]] = {}

        # build trajectories per day
        for time, roi in values:
            day = time.date()
            if day in day_trajectories:
                if roi.name != day_trajectories[day][-1].name:  # avoids repetitions
                    day_trajectories[day].append(roi)
            else:
                day_trajectories[day] = [roi]

        # filter based on trajectory length
        result = {}
        for day in day_trajectories:
            dated_traj = day_trajectories[day]
            if len(dated_traj) >= self.min_trajectory_length:
                result[day] = dated_traj
        return result
