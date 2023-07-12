import json
from datetime import datetime

from parsoda import SocialDataItem
from parsoda.model import Parser

from parsoda.model.social_data_item import SocialDataItemBuilder


class TwitterParser(Parser):

    def __call__(self, text_line):
        try:
            json_dict = json.loads(text_line)

            builder = SocialDataItemBuilder() \
                .set_original_format('twitter/2017') \
                .set_id(json_dict['id']) \
                .set_user_id(json_dict['user']['id']) \
                .set_user_name(json_dict['user']['name']) \

            try:
                if 'date' in json_dict:
                    date_posted = datetime.strptime(json_dict['date'], '%a %b %d %H:%M:%S +0000 %Y')
                    builder.set_date_posted(date_posted)
            except:
                pass

            if 'text' in json_dict:
                builder.set_text(json_dict['text'])

            if 'hashtags' in json_dict:
                builder.set_tags(json_dict['hashtags'])

            if 'location' in json_dict:
                location = json_dict['location']
                if 'latitude' in location and 'longitude' in location:
                    latitude = float(location['latitude'])
                    longitude = float(location['longitude'])
                    builder.set_location(latitude, longitude)

            return builder.build()
        except Exception as e:
            print(e)
            return None
