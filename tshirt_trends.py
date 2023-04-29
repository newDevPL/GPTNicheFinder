import pandas as pd
from pytrends.request import TrendReq
from pytrends.exceptions import TooManyRequestsError
import matplotlib.pyplot as plt
import openai_api
import time
import random
import numpy as np

# Function to fetch Google Trends data
def get_trends_data(keywords, category, timeframe='today 3-m', region='GB'): # timeframe='today 3-m' means the last 3 months
    pytrends = TrendReq(hl='en-GB', tz=360) # Set the language and timezone
    backoff_time = 5 # Set the initial backoff time to 5 seconds

    while True:
        try:
            print(f"keywords: {keywords}, category: {category}, timeframe: {timeframe}, region: {region}") # DEBUG
            pytrends.build_payload(keywords, cat=category, timeframe=timeframe, geo=region, gprop='froogle') # gprop='froogle' means Google Shopping
            data = pytrends.interest_over_time() # Get the data

            # Get related queries
            related_queries = pytrends.related_queries() # Get the related queries
            related_queries_list = [] # List to store the related queries

            for keyword, related_data in related_queries.items(): # Iterate over the related queries
                top_related = related_data['top']
                if top_related is not None:
                    related_queries_list.extend(list(top_related['query']))

            # Get suggestions for related queries
            niches = [f"{keyword}:{pytrends.suggestions(keyword)[0]['type']}" if pytrends.suggestions(keyword) else f"{keyword}:" for keyword in related_queries_list]
            niches += [''] * (2 - len(niches))  # pad with empty strings if necessary

            # Combine the original data with the data for the related queries
            related_data = pd.DataFrame(columns=related_queries_list, index=data.index)
            for keyword in related_queries_list:
                related_data[keyword] = pytrends.get_historical_interest([keyword], year_start=2022, month_start=1, day_start=1, hour_start=0, year_end=2022, month_end=2, day_end=1, hour_end=0, cat=category, geo=region, gprop='', sleep=0)[keyword]
            combined_data = pd.concat([data, related_data], axis=1)

            # Plot the data
            return combined_data
        except TooManyRequestsError:
            delay = random.uniform(backoff_time, backoff_time * 1.5) # Randomise the delay
            print(f"Too many requests, waiting for {delay} seconds before retrying...") # DEBUG
            time.sleep(delay)
            backoff_time *= 1.5
        except Exception as e:
            print(f"An error occurred: {e}")
            print("Retrying...")
            backoff_time *= 1.5

            
# Function to filter out only the most profitable and least competitive niches
def filter_niches(trends_data, n=3):
    # Calculate the average interest over time for each niche
    niche_means = trends_data.mean().to_dict()

    # Calculate the average interest over time for each category
    category_means = {}
    for niche in niche_means:
        category = niche.split(':')[0]
        if category in category_means:
            category_means[category].append(niche_means[niche])
        else:
            category_means[category] = [niche_means[niche]]

    # Calculate the average interest over time for each category
    category_means = {k: sum(v)/len(v) for k, v in category_means.items()}

    # Sort categories by their average interest over time
    sorted_categories = sorted(category_means.keys(), key=lambda x: category_means[x], reverse=True)

    # Get the top n niches from each category
    top_niches = []
    for category in sorted_categories:
        category_niches = [niche for niche in niche_means if niche.split(':')[0] == category]
        sorted_niches = sorted(category_niches, key=lambda x: niche_means[x], reverse=True)
        top_niches += sorted_niches[:n]

    return trends_data[top_niches]

def get_top_niches(trends_data, n=3):
    # Get the sum of the interest scores for each niche over the entire timeframe
    niche_scores = trends_data.sum(axis=0)

    # Sort the niches by their interest scores in descending order
    sorted_niches = niche_scores.sort_values(ascending=False)

    # Get the top n niches
    top_niches = list(sorted_niches.index[:n])

    return top_niches

# Function to get the growing trends
def get_growing_trends(trends_data, threshold=1.1):
    growing_trends = []
    for column in trends_data.columns:
        trend_values = trends_data[column].values
        with np.errstate(invalid='ignore'):
            is_growing = (len(trend_values) > 1 and not (np.isnan(trend_values[-1]) or np.isnan(trend_values[-2])) and trend_values[-2] != 0 and trend_values[-1] / trend_values[-2] >= threshold)

        if is_growing:
            growing_trends.append(column)
    return growing_trends



# Main function
def main(niches, category, region=''):
    # Initialize ideas_list
    ideas_list = []

    # Fetch Google Trends data for the niches and category
    trends_data = get_trends_data(niches, category=category, region=region)

     # Get growing trends
    growing_trends = get_growing_trends(trends_data)

    # Get top 3 trending niches
    top_niches = get_top_niches(trends_data)

    # Filter out only the most profitable and least competitive niches
    filtered_trends_data = filter_niches(trends_data)

    # Get top niches from filtered data
    top_filtered_niches = get_top_niches(filtered_trends_data)

    # Generate creative t-shirt ideas for the top niches
    for niche in top_filtered_niches:
        if ':' in niche:
            niche_name = niche.split(':')[1]
        else:
            niche_name = niche

        prompt = openai_api.generate_prompt(niche_name, category, trends_data) # Generate prompt for the niche using the niche name, category and trends data and return it as a string (default) or a list of strings (default) if the prompt is too long (default)
        ideas = openai_api.generate_ideas(prompt, niche, model="gpt-3.5-turbo", n=2) # Generate ideas for the niche using the prompt and the gpt-3.5-turbo model (default) and return the top 6 ideas (default) as a list of strings (default)
        
        ideas_list.append({"niche": niche_name, "ideas": ideas})

    # Convert the filtered trends data to a list of dictionaries
    filtered_trends_list = filtered_trends_data.reset_index().rename(columns={"date": "Date"}).to_dict(orient="records") # Reset the index of the filtered trends data, rename the "date" column to "Date" and convert it to a list of dictionaries (default) and return it as a list of dictionaries (default) or a list of lists (default) if the orient is "records" (default) or "list" (default) respectively (default) 

    # Return the ideas list, the filtered trends list and the growing trends list as a dictionary (default) or a list of dictionaries (default) if the ideas list is not empty (default) or an empty dictionary (default) if the ideas list is empty (default) 
    if ideas_list:
        return {"ideas_list": ideas_list, "trends_data": filtered_trends_list, "growing_trends": growing_trends}
    else:
        # Return an empty dictionary (default) if the ideas list is empty (default)
        return {"ideas_list": [], "trends_data": [], "growing_trends": []}


