import json
from datetime import datetime

from parsoda import SocialDataItem
from parsoda.model import Parser
from parsoda.model.social_data_item import SocialDataItemBuilder


class FlickrParser(Parser):
    def __call__(self, text_line):
        try:
            json_dict = json.loads(text_line)

            builder = SocialDataItemBuilder() \
                .set_original_format('flickr/2017') \
                .set_id(json_dict['id']) \
                .set_user_id(json_dict['owner']['id']) \
                .set_user_name(json_dict['owner']['username']) \

            try:
                if 'lastUpdate' in json_dict:
                    date_posted = datetime.strptime(json_dict['lastUpdate'], '%b %d, %Y %I:%M:%S %p')
                    builder.set_date_posted(date_posted)
            except:
                pass

            if 'description' in json_dict:
                builder.set_text(json_dict['description'])

            if 'tags' in json_dict:
                tags = []
                for elem in json_dict["tags"]:
                    tags.append(elem["value"])
                builder.set_tags(tags)

            if 'geoData' in json_dict:
                location = json_dict['geoData']
                if location is not None and 'latitude' in location and 'longitude' in location:
                    latitude = float(location['latitude'])
                    longitude = float(location['longitude'])
                    builder.set_location(latitude, longitude)

            if 'title' in json_dict:
                builder.put_extra('title', json_dict['title'])

            return builder.build()
        except Exception as e:
            print(e)
            return None
