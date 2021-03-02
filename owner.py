"""owner.py
Obtain land ownership info from SITLA web feature service
using lat,lon coordinates to query REST endpoint
"""

__author__ = "Justin Johnson"
__email__ = "authalic@gmail.com"
__date__ = "02 Mar, 2021"
__version__ = "1.0"
__status__ = "Production"

import argparse
import requests
import json


# configure command-line parsing of input coordinates

parser = argparse.ArgumentParser()
parser.add_argument("lat", help="Latitude of point coordinate (WGS84)")
parser.add_argument("lon", help="Longitude of point coordinate (WGS84)")

args = parser.parse_args()

# options:
# consider adding support for different SRIDs
# use the pyproj module: https://pyproj4.github.io/pyproj/stable/#

SITLA_URL = r"https://gis.trustlands.utah.gov/server/rest/services/Ownership/UT_SITLA_Ownership_LandOwnership/FeatureServer/0/query"

payload = {
    'where': '1=1',
    'objectIds': '',
    'time': '',
    'geometry': args.lon + ',' + args.lat,
    'geometryType': 'esriGeometryPoint',
    'inSR': '4326',
    'spatialRel': 'esriSpatialRelIntersects',
    'distance': '',
    'units': 'esriSRUnit_Foot',
    'relationParam': '',
    'outFields': '*',
    'returnGeometry': 'false',
    'maxAllowableOffset': '',
    'geometryPrecision': '',
    'outSR': '',
    'havingClause': '',
    'gdbVersion': '',
    'historicMoment': '',
    'returnDistinctValues': 'false',
    'returnIdsOnly': 'false',
    'returnCountOnly': 'false',
    'returnExtentOnly': 'false',
    'orderByFields': '',
    'groupByFieldsForStatistics': '',
    'outStatistics': '',
    'returnZ': 'false',
    'returnM': 'false',
    'multipatchOption': 'xyFootprint',
    'resultOffset': '',
    'resultRecordCount': '',
    'returnTrueCurves': 'false',
    'returnExceededLimitFeatures': 'false',
    'quantizationParameters': '',
    'returnCentroid': 'false',
    'sqlFormat': 'none',
    'resultType': '',
    'featureEncoding': 'esriDefault',
    'datumTransformation': '',
    'f': 'pjson',
    }

# send the request to the endpoint
r = requests.get(SITLA_URL, params=payload)

# decode JSON
j = r.json()

# print(json.dumps(j, indent=4, sort_keys=False))

# check if the response was unable to perform query
if ("error" in j):

    print("Error:", j['error']["message"])
    for error in (j['error']['details']):
        print('Details: ' + error)

else:

    # get the dict of attributes from response
    attribs = j['features'][0]['attributes']

    # print(json.dumps(attribs, indent=4, sort_keys=False))

    # print("Owner Agency Admin")
    print(attribs["OWNER"], attribs["AGENCY"], attribs["ADMIN"])
