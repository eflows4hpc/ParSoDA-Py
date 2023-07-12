

from datetime import datetime
from pathlib import Path
import random
import string
from typing import List, Set, Tuple
from parsoda.model.social_data_item import SocialDataItemBuilder

from roi import RoI, load_RoIs

def random_string(length: int):
    return ''.join(random.choice(string.ascii_lowercase) for i in range(length))

def random_text():
    return random_string(30)

def random_tags(length: int):
    num_chars = len(str(length))
    tags = set()
    while len(tags) < length:
        tags.add(random_string(num_chars))
    return list(tags)

def estimated_item_size(rois):
    item = random_item(0, 100, random_tags(1000), rois)
    return len(item.to_json())
        

def random_item(id, users: int, tags: List[str], rois: List[RoI], builder = SocialDataItemBuilder()):
    user_id = random.randrange(0, users)
    tag1 = tags[random.randrange(0, len(tags))]
    tag2 = tags[random.randrange(0, len(tags))]
    tag3 = tags[random.randrange(0, len(tags))]
    roi = rois[random.randrange(0, len(rois))]
    roi_centroid = roi.get_center()
    
    return builder \
        .set_original_format('parsoda-item') \
        .set_id(id) \
        .set_user_id(user_id) \
        .set_user_name(f"{user_id:010}") \
        .set_date_posted(datetime.fromtimestamp(random.randrange(1499097285,1688399653))) \
        .set_text(random_string(30)) \
        .set_tags([tag1, tag2, tag3]) \
        .set_location(roi_centroid.x, roi_centroid.y) \
        .build()


def generate_dataset(dimension: str, roi_file_path: Path, output_path: Path)->None:
    rois = load_RoIs(roi_file_path)
    
    if dimension.endswith('g') or dimension.endswith("G"):
        dimension_bytes = int(dimension[:-1])*1024*1024*1024
    elif dimension.endswith('m') or dimension.endswith("M"):
        dimension_bytes = int(dimension[:-1])*1024*1024
    elif dimension.endswith('k') or dimension.endswith("K"):
        dimension_bytes = int(dimension[:-1])*1024
    elif dimension.endswith('b') or dimension.endswith("B"):
        dimension_bytes = int(dimension[:-1])
    else:
        dimension_bytes = int(dimension)
    
    estimated_row_size = estimated_item_size(rois)+1
    estimated_num_items = int(dimension_bytes/estimated_row_size)
    
    users: int = int(estimated_num_items*0.5)
    tags: List[str] = random_tags(1000)
    
    builder = SocialDataItemBuilder()

    with open(output_path, "w") as out:
        id=0
        current_dimension=0
        while current_dimension < dimension_bytes:
            item = random_item(id, users, tags, rois, builder)
            json_row = f"{item.to_json()}\n"
            out.write(json_row)
            
            id+=1
            current_dimension += len(json_row)
            
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser("ParSoDA Dataset Generator")
    parser.add_argument(
        "dimension",
        type=str,
        help="desired dataset dimension ending with a character indicating the metric:\n"
        "- 'g' or 'G' for Gigabytes"
        "- 'm' or 'M' for Megabytes"
        "- 'k' or 'K' for Kilobytes"
        "- 'b' or 'B' or nothing for Bytes"
    )
    parser.add_argument(
        "roi_file_path",
        type=Path,
        help="Regions of Interest KML file path"
    )
    parser.add_argument(
        "output_path",
        type=Path,
        help="output JSON dataset file path"
    )
    args = parser.parse_args()
    generate_dataset(**vars(args))