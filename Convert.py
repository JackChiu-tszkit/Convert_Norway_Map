import pyproj
import json
import numpy
from math import ceil
import sys
if __name__ == "__main__":
    arguments = sys.argv
    #input_file = sys.argv[1]
    #output_file = sys.argv[2]
    coordinates_per_object = 2000
    keep_all = True
    source = pyproj.Proj(proj='utm', zone=33, ellps='WGS84')
    target = pyproj.Proj(init='EPSG:4326')
    input_file="Fylker.geojson"
    with open(input_file, 'r') as f:
        data = json.load(f)
    data['crs']['properties']['name'] = "EPSG::4326"
    print(data['crs']['properties']['name'])
    for feature in data['features']:
        coords = feature['geometry']['coordinates']
        print(coords)
        newCoordLists = []
        for coordList in coords:
            print(len(coordList))
            step = int(ceil(len(coordList) / coordinates_per_object))
            newCoordList = []
            counter = 0
            for coordPair in coordList:
                if keep_all or counter % step == 0 or counter + 1 == len(coordList):
                    x1 = coordPair[0]
                    y1 = coordPair[1]
                    #do transformation
                    x, y = pyproj.transform(source,target,x1, y1) #重点
                    #print(coordPair[0], coordPair[1])
                    x, y = source(x1, y1, inverse=True)
                    #print(x, y)
                    newCoordList.append([x, y])
                counter += 1
            newCoordLists.append(newCoordList)
        feature['geometry']['coordinates'] = newCoordLists

    output_file="fylker_convert.geojson"
    with open(output_file, 'w') as f:
        f.write(json.dumps(data))