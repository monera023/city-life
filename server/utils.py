from typing import List

from server.constants import Category, CategoryPlaces, Place


def get_formatted_category(items):
    resp = []
    for item in items:
        resp.append(Category(id=item[0], name=item[1], emoji=item[2]))
    return resp


def get_formatted_place_category(items):
    category_places_map = {}
    resp = []
    for item in items:
        if item[0] in category_places_map:
            category_places_map[item[0]]['places'].append(Place(name=item[2], url=item[3], category=item[0]))
        else:
            category_places_map[item[0]] = {'places': [Place(name=item[2], url=item[3], category=item[0])], 'emoji': item[1]}

    for key, value in category_places_map.items():
        resp.append(CategoryPlaces(category_name=key, category_emoji=value['emoji'], places=value['places']))
    return resp


