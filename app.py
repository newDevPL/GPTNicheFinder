from flask import Flask, render_template, request, session, redirect, url_for, flash
import tshirt_trends
from tshirt_trends import get_top_niches
import os
from utils import get_regions
from config import IP_ADDRESS, PORT
import config

app = Flask(__name__)
app.secret_key = os.urandom(24)


@app.route("/", methods=["GET", "POST"])
def index():
    regions = get_regions()

    if request.method == "POST":
        niche_input = request.form["niche_input"]
        model_choice = request.form["model_choice"]
        region = request.form.get('region')
        timeframe = request.form['timeframe']  # Get the selected timeframe from the form
        niches = [niche.strip() for niche in niche_input.split(",")]
        if len(niches) > 5:
            flash("Please enter up to 5 niches separated by commas.")
            return redirect(url_for("index"))
        print(f"Detected more than 5 niches, please select up to 5 niches!")
        
        results = tshirt_trends.main(niches, 428, region=region, model_choice=model_choice, timeframe=timeframe) # Use 428 for "T-Shirts". You can lookup categories in the static/categories.json file

        # Filter out None values from ideas_list
        ideas_list = [x for x in results["ideas_list"] if x is not None]

        # Store form data in session
        session['niche_input'] = niche_input
        session['model_choice'] = model_choice
        session['region'] = region
        session['timeframe'] = timeframe

        return render_template("index.html", ideas_list=results["ideas_list"], trends_data=results["trends_data"], regions=regions)  # Pass the ideas_list and trends_data to the template for rendering the results in the browser

    # Load form data from session if it exists
    niche_input = session.get('niche_input', '')
    model_choice = session.get('model_choice', '')
    region = session.get('region', '')
    timeframe = session.get('timeframe', '')

    return render_template("index.html", regions=regions, niche_input=niche_input, model_choice=model_choice, region=region, timeframe=timeframe, openai_api_key=config.OPENAI_API_KEY, 
        local_model_file=config.MML_MODEL_FILE)

if __name__ == "__main__":
    app.run(host=IP_ADDRESS, debug=True, port=PORT)  # Change this to match the IP address of your computer, select custom port if needed
