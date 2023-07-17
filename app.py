from flask import Flask, render_template, jsonify
import psycopg2
import geojson
from shapely import wkb
import config

app = Flask(__name__)

# precompile wkb loading function
load_wkb = wkb.loads

def to_geojson(parish, pm2_5, wkb_string, id):
    geometry = load_wkb(wkb_string)
    feature = geojson.Feature(id=str(id), geometry=geometry, properties={
                              "parish": parish, "pm2_5": pm2_5})
    return feature

offset = 0 # Global variable to keep track of current offset

@app.route('/')
def index():
    return render_template("index.html")


@app.route('/map')
def get_map():
    global offset
    
    conn = psycopg2.connect(database=config.DATABASE, user=config.USER,
                            password=config.PASSWORD, host=config.HOST, port=config.PORT)
    # create cursor object
    cur = conn.cursor()
    
    chunk_size = 50

    cur.execute(f"SELECT COUNT(*) FROM airqo_data")
    # total_rows = cur.fetchone()[0]
    total_rows = 500


    # cur.execute('''SELECT parish, pm2_5, geometry FROM airqo_data''')
    cur.execute('''SELECT parish, pm2_5, geometry FROM airqo_data rows LIMIT 30 OFFSET 0''')
    rows = cur.fetchall()  # fetch all rows 
    
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
    
    features = [ to_geojson(row[0], round(row[1]), row[2], id=i) for i, row in enumerate(rows) if i < 10000 ]
    
    feature_collection = geojson.FeatureCollection(features)
    cur.close()
    conn.close()
    print('Returning feature collection')
    return jsonify(feature_collection)


if __name__ == "__main__":
    app.run(debug=True)
