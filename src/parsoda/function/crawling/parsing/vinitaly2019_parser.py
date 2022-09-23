import json
from datetime import datetime

from parsoda import SocialDataItem
from parsoda.model import Parser

from parsoda.model.social_data_item import SocialDataItemBuilder


class Vinitaly2019Parser(Parser):

    def __call__(self, text_line):
        try:
            json_dict = json.loads(text_line)

            builder = SocialDataItemBuilder() \
                .set_original_format('vinitaly/2019') \
                .set_id(json_dict['id']) \
                .set_user_id(json_dict['user_id']) \
                .set_user_name(json_dict['username'])

            try:
                if 'date' in json_dict:
                    date_posted = datetime.strptime(json_dict['date'], '%a %b %d %H:%M:%S +0000 %Y')
                    builder.set_date_posted(date_posted)
            except:
                pass

            if 'tweet' in json_dict:
                builder.set_text(json_dict['tweet'])

            if 'hashtags' in json_dict:
                builder.set_tags(json_dict['hashtags'])

            return builder.build()
        except Exception as e:
            print(f"Exception thrown in 'Vinitaly2019Parser': {e}")
            return None
