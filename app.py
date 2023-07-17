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
    feature = geojson.Feature(id=str(id), geometry=geometry, properties={"parish": parish, "pm2_5": pm2_5})
    return feature

offset = 0 # Global variable to keep track of current offset

@app.route('/')
def index():
    return render_template("index.html")


@app.route('/map')
def get_map():
    global offset
    
    # connect to database
    conn = psycopg2.connect(database=config.DATABASE, user=config.USER,
                            password=config.PASSWORD, host=config.HOST, port=config.PORT)
    # create cursor object
    cur = conn.cursor()
    
    chunk_size = 50

    cur.execute(f"SELECT COUNT(*) FROM airqo_data")
    # total_rows = cur.fetchone()[0]                    # Get total number of rows in table
    total_rows = 500

    if offset < total_rows:
        cur.execute(f"SELECT parish, pm2_5, geometry FROM airqo_data LIMIT {chunk_size} OFFSET {offset}")
        rows = cur.fetchall()
        features = [to_geojson(row[0], round(row[1]), row[2], id=i+offset) for i, row in enumerate(rows)]
        feature_collection = geojson.FeatureCollection(features)
        # offset += chunk_size
        offset = offset + chunk_size
        print('finished that chunk')
        print(f'Current Offset: {offset}')
        
    else:
        feature_collection = geojson.FeatureCollection([])  # Empty feature collection if no more rows

    cur.close()
    conn.close()
    print('Returning feature collection')
    return jsonify(feature_collection)


if __name__ == "__main__":
    app.run(debug=True)
