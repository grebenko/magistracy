import Levenshtein
from mediawiki import MediaWiki
import json
import sys
reload(sys)
sys.setdefaultencoding('utf8')
wikipedia = MediaWiki(lang='ru')
result_data = []
i = 0

with open("export.geojson", "r") as read_file:
    data = json.load(read_file)

    for feat in data['features']:
        data_found = False
        p = ''

        if "wikipedia" in feat['properties']:
            p = wikipedia.page(feat['properties']['wikipedia'])
            data_found = True
        else:
            try:
                geo = wikipedia.geosearch(latitude=feat['geometry']['coordinates'][1], longitude=feat['geometry']['coordinates'][0])
                for geo_res in geo:
                    if Levenshtein.distance(geo_res, feat['properties']['name']) <= 3:
                        p = wikipedia.page(geo_res)
                        data_found = True
                        break
            except KeyError:
                try:
                    name_search = wikipedia.search(feat['properties']['name'])
                    for name_res in name_search:
                        if Levenshtein.distance(geo_res, feat['properties']['name']) <= 3:
                            p = wikipedia.page(name_res)
                            data_found = True
                            break
                except KeyError:
                    p = ''
        if data_found:
            result_data.append(feat)
            result_data[i]['wiki_summary'] = p.summary
            result_data[i]['wiki_catrgories'] = p.categories
            result_data[i]['wiki_images'] = p.images
            i += 1

    with open("geo.json", "w") as write_file:
        json.dump(result_data, write_file)