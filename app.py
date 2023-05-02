from flask import Flask, render_template, request
import tshirt_trends
from tshirt_trends import get_top_niches

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        niche_input = request.form["niche_input"]
        model_choice = request.form["model_choice"]
        niches = [niche.strip() for niche in niche_input.split(",")]

        results = tshirt_trends.main(niches, 428, model_choice=model_choice) # Use 428 for "T-Shirts". You can lookup categories in the static/categories.json file
# Filter out None values from ideas_list
        ideas_list = [x for x in results["ideas_list"] if x is not None]
        return render_template("index.html", ideas_list=results["ideas_list"], trends_data=results["trends_data"]) # Pass the ideas_list and trends_data to the template for rendering the results in the browser

    return render_template("index.html")

if __name__ == "__main__":
    app.run(host='192.168.0.10', debug=True, port=8081) # Change this to match the IP address of your computer, select custom port if needed
