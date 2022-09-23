# coding=utf-8
import json

from parsoda_costantino.common.item.TwitterItem import TwitterItem
from parsoda_costantino.common.item import FlickrItem
import time
import os





def map_json(line_in):
    try:
        ab = FlickrItem(line_in)
        return ab
    except:
        return None


def remove_service_file():
    path_service_file = "./resources/serviceFile.json"
    if os.path.exists(path_service_file):
        os.remove(path_service_file)


def get_service_file():
    path_service_file = "./resources/serviceFile.json"
    return path_service_file


def add_to_service_file(fileIn):
    num_elements = 0

    path_service_file = "./resources/serviceFile.json"

    with open(path_service_file, 'a') as f:
        for line in open(fileIn, 'r'):
            try:
                f.write(line)
                num_elements += 1
            except:
                pass
    f.close()
    return num_elements


def loadJsons(fileIn, type):
    jsons = []
    for line in open(fileIn, 'r'):
        try:
            jsons.append((line, type))
        except:
            pass
    return jsons


def readJsons(listIn):
    jsons = []
    for line, type in listIn:
        try:
            jsons.append((json.loads(line), type))
        except:
            pass
    return jsons


def create_AbstractGeotaggedItems(line):
    try:
        jsonEl = json.loads(line)
    except Exception:
        return None
    try:
        return FlickrItem(jsonEl)
    except Exception:
        pass
    try:
        return TwitterItem(jsonEl)
    except Exception as e:
        pass
    return None


"""
Le funzioni di crawling restituiscono una lista di tuple del tipo:
    (stringa che rappresenta il json del post, tipo del social usato)
    il tipo del social viene passato a runtime e puo essere "Flickr" e "Twitter"
    al momento.
    Questa funziona legge il json stringa, crea la versione python del json e
    crea l'opportuno abstract_geotagged_item
"""


def create_abstract_objects(list_json):
    data = readJsons(list_json)

    items = []
    for tuple in data:
        if tuple[1] == "Flickr":
            items.append(FlickrItem(tuple[0]))
        elif tuple[1] == "Twitter":
            items.append(TwitterItem(tuple[0]))
    data = None

    return items


def printJsons(jsons):
    for element in jsons:
        print((json.dumps(element, indent=4, separators=(". ", " = "), sort_keys=True)))
