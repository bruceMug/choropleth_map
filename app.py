from flask import Flask, render_template, jsonify
import psycopg2
import geojson
from shapely import wkb
import config

from timeit import default_timer as timer           # for timing the code

app = Flask(__name__)

# precompile wkb loading function
load_wkb = wkb.loads

def to_geojson(parish, pm2_5, wkb_string, id):
    # geometry = wkb.loads(bytes.fromhex(wkb_string))
    geometry = load_wkb(wkb_string)
    feature = geojson.Feature(id=str(id), geometry=geometry, properties={
                              "parish": parish, "pm2_5": pm2_5})
    return feature


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/map')
def get_map():
    conn = psycopg2.connect(database=config.DATABASE, user=config.USER,
                            password=config.PASSWORD, host=config.HOST, port=config.PORT)

    # create cursor object
    cur = conn.cursor()
    start = timer()                 # start timer   # todo : remove this
    cur.execute('''SELECT parish, pm2_5, geometry FROM airqo_data''')
    
    rows = cur.fetchall()  # fetch all rows

    end = timer()                                                       # end timer     # todo : remove this
    print("Fetch row time: ", end - start)                            # todo : remove this
    
    start = timer()                                                     # start timer   # todo : remove this
    """
    features = []
    i = 0
    for row in rows:
        if i < 1000:
            parish = row[0]
            pm2_5 = row[1]
            geometry = row[2]
            i = i+1
            features.append(to_geojson(parish, round(pm2_5), geometry, id=i)) """
    
    features = [to_geojson(row[0], round(row[1]), row[2], id=i) for i, row in enumerate(rows) if i < 1000]
    
    end = timer()                                                      # end timer     # todo : remove this
    print("Geojson collection time: ", end - start)                              # todo : remove this
    
    feature_collection = geojson.FeatureCollection(features)
    # print(feature_collection)
    # todo : check the features of all the rows
    
    # f = open('parish_data_2000.json', 'w')
    # f.write(feature_collection.__str__())
    # f.close()

    cur.close()
    conn.close()
    return jsonify(feature_collection)


if __name__ == "__main__":
    app.run(debug=True)
