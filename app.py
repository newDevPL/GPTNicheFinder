from flask import Flask, render_template, request
import tshirt_trends
from tshirt_trends import get_top_niches

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        niche_input = request.form["niche_input"]
        niches = [niche.strip() for niche in niche_input.split(",")]

        results = tshirt_trends.main(niches, 428) # Use 428 for "T-Shirts"
        return render_template("index.html", ideas_list=results["ideas_list"], trends_data=results["trends_data"])

    return render_template("index.html")

if __name__ == "__main__":
    app.run(host='192.168.0.10', debug=True, port=8081)
