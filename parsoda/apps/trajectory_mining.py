from typing import List

from parsoda import SocialDataApp
from parsoda.function.analysis.gap_bide_analysis import GapBIDE
from parsoda.function.filtering import IsInRoI

from parsoda.function.mapping.find_poi import FindPoI
from parsoda.function.reduction.reduce_by_trajectories import ReduceByTrajectories
from parsoda.function.visualization.sort_gap_bide import SortGapBIDE
from parsoda.model.driver.parsoda_driver import ParsodaDriver
from parsoda.model.function.crawler import Crawler

# do not use lambda, they cannot be pickled
def __secondary_key(x):
    return x[0]

def parsoda_trajectory_mining(
    rois_file: str,
    *,
    crawlers: List[Crawler] = [],
    min_trajectory_length=3,  
    min_support=1, 
    min_gap=0, 
    max_gap=10, 
    visualization_file="trajectory_mining.txt",
    visualization_min_length=3
) -> SocialDataApp:  
    app = SocialDataApp("Trajectory Mining")
    app.set_crawlers(crawlers)
    app.set_filters([
        IsInRoI(rois_file)
    ])
    app.set_mapper(FindPoI(rois_file))
    app.set_secondary_sort_key(__secondary_key)
    app.set_reducer(ReduceByTrajectories(min_trajectory_length))
    app.set_analyzer(GapBIDE(min_support, min_gap, max_gap))
    app.set_visualizer(
        SortGapBIDE(
            visualization_file, 
            'support', 
            mode='descending', 
            min_length=visualization_min_length
        )
    )
    return app
