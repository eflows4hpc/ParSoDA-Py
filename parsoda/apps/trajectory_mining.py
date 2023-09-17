from typing import List

from parsoda import SocialDataApp
from parsoda.function.analysis.gap_bide_analysis import GapBIDE
from parsoda.function.filtering import IsInRoI

from parsoda.function.mapping.find_poi import FindPoI
from parsoda.function.reduction.reduce_by_trajectories import ReduceByTrajectories
from parsoda.function.visualization.sort_gap_bide import SortGapBIDE
from parsoda.model.driver.parsoda_driver import ParsodaDriver
from parsoda.model.function.crawler import Crawler


def build_trajectory_mining(
    driver: ParsodaDriver,
    crawlers: List[Crawler],
    rois_file: str,
    *, 
    num_partitions=-1, 
    chunk_size=64, 
    min_trajectory_length=3,  
    min_support=1, 
    min_gap=0, 
    max_gap=10, 
    visualization_file="trajectory_mining.txt",
    visualization_min_length=3
):  
    app = SocialDataApp("Trajectory Mining", driver, num_partitions=num_partitions, chunk_size=chunk_size)
    app.set_crawlers(crawlers)
    app.set_filters([
        IsInRoI(rois_file)
    ])
    app.set_mapper(FindPoI(rois_file))
    app.set_secondary_sort_key(lambda x: x[0])
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
