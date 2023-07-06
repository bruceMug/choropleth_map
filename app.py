from flask import Flask, render_template, jsonify
import psycopg2
import geojson
from shapely import wkb

app = Flask(__name__)


def to_geojson(parish, pm2_5, wkb_string):
    geometry = wkb.loads(bytes.fromhex(wkb_string))
    feature = geojson.Feature(geometry=geometry, properties={
                              "parish": parish, "pm2_5": pm2_5})
    return feature


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/map')
def get_map():
    conn = psycopg2.connect(database="airqo", user="postgres",
                            password="user", host='localhost', port='5432')

    # create cursor object
    cur = conn.cursor()
    cur.execute('''SELECT parish, pm2_5, geometry FROM airqo_data''')
    # cur.execute('''SELECT parish, population_density FROM airqo_data''')
    rows = cur.fetchall()  # fetch all rows

    print(len(rows))
    features = []
    i = 0
    for row in rows:
        if i < 2:
            parish = row[0]
            pm2_5 = row[1]
            geometry = row[2]
            
            features.append(to_geojson(parish, round(pm2_5), geometry))
            i = i+1

    feature_collection = geojson.FeatureCollection(features)
    
    
    # data_map = [{'parish':row[0], 'population_density':row[1]} for row in rows]

    cur.close()
    conn.close()
    # return render_template("index.html", data=feature_collection)
    return jsonify(feature_collection)


if __name__ == "__main__":
    app.run(debug=True)
