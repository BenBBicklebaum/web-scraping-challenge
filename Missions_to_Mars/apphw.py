from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape
import pymongo

# Create an instance of Flask
app = Flask(__name__)

# Setup connection to mongodb
conn = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn)

# Select database and collection to use
db = client.mars
collection = db.marsscrape

# Route to render index.html template using data from Mongo
@app.route("/")
def home():

    # Find the record of data from the mongo database
    mars_data = collection.find_one()
    # Return template and data
    return render_template("index.html", mars=mars_data)


# Route that will trigger the scrape function
@app.route("/scrape")
def app_scrape():

    # Run the scrape function, drop the current collection, & create a new collection and insert the data
    mars_func = scrape.scrape()
    collection.drop()
    collection.insert_one(mars_func)

    # Redirect back to home page
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)