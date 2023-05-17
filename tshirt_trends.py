import pandas as pd
from pytrends.request import TrendReq
from pytrends.exceptions import TooManyRequestsError
import matplotlib.pyplot as plt
import openai_api
import time
import random
import numpy as np
from sklearn.linear_model import LinearRegression

# Function to fetch Google Trends data
def get_trends_data(keywords, category, timeframe='today 12-m', region='US'): # timeframe='today 3-m' means the last 3 months
    pytrends = TrendReq(hl='en-GB', tz=360) # Set the language and timezone
    backoff_time = 5 # Set the initial backoff time to 5 seconds

    while True:
        try:
            print(f"Fetching trends data for keywords: {keywords}, category: {category}, timeframe: {timeframe}, region: {region}") # DEBUG
            pytrends.build_payload(keywords, cat=category, timeframe=timeframe, geo=region, gprop='froogle') # gprop='froogle' means Google Shopping
            data = pytrends.interest_over_time() # Get the data
            print("Fetched interest over time data.") # DEBUG

            # Get related queries
            print("Fetching related queries...") # DEBUG
            related_queries = pytrends.related_queries() # Get the related queries
            related_queries_list = [] # List to store the related queries

            for keyword, related_data in related_queries.items(): # Iterate over the related queries
                top_related = related_data['top']
                if top_related is not None:
                    related_queries_list.extend(list(top_related['query']))
            print(f"Related queries: {related_queries_list}") # DEBUG

            # Get suggestions for related queries
            print("Fetching suggestions for related queries...") # DEBUG
            niches = [f"{keyword}:{pytrends.suggestions(keyword)[0]['type']}" if pytrends.suggestions(keyword) else f"{keyword}:" for keyword in related_queries_list]
            niches += [''] * (2 - len(niches))  # pad with empty strings if necessary
            print(f"Suggestions for related queries: {niches}") # DEBUG

            # Combine the original data with the data for the related queries
            print("Combining the original data with the data for the related queries...") # DEBUG
            related_data = pd.DataFrame(columns=related_queries_list, index=data.index)
            for keyword in related_queries_list:
                related_data[keyword] = pytrends.get_historical_interest([keyword], year_start=2022, month_start=1, day_start=1, hour_start=0, year_end=2022, month_end=2, day_end=1, hour_end=0, cat=category, geo=region, gprop='', sleep=0)[keyword]
            combined_data = pd.concat([data, related_data], axis=1)
            print("Combined data ready.") # DEBUG

            # Return the data
            return combined_data
        except TooManyRequestsError:
            delay = random.uniform(backoff_time, backoff_time * 1.5) # Randomise the delay
            print(f"Too many requests, waiting for {delay} seconds before retrying...") # DEBUG
            time.sleep(delay)
            backoff_time *= 1.5
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            print("Retrying...")
            backoff_time *= 1.5


            
# Function to filter out only the most profitable and least competitive niches
def filter_niches(trends_data, n=3):
    print(f"Filtering niches from trends data with n={n}...") # DEBUG

    # Calculate the average interest over time for each niche
    niche_means = trends_data.mean().to_dict()

    # Remove 'isPartial' from the dictionary
    niche_means.pop('isPartial', None)
    print(f"Calculated means for niches: {niche_means}") # DEBUG

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
    print(f"Calculated means for categories: {category_means}") # DEBUG
    
    niche_trends = {niche: get_trend_slope(trends_data[niche]) for niche in niche_means}
    print(f"Calculated trends for niches: {niche_trends}") # DEBUG

    # Sort categories by their average interest over time
    sorted_categories = sorted(category_means.keys(), key=lambda x: category_means[x], reverse=True)
    print(f"Sorted categories: {sorted_categories}") # DEBUG

    # Get the top n niches from each category
    top_niches = []
    for category in sorted_categories:
        category_niches = [niche for niche in niche_means if niche.split(':')[0] == category]
        sorted_niches = sorted(category_niches, key=lambda x: niche_means[x], reverse=True)
        top_niches += sorted_niches[:n]
        print(f"Top {n} niches for category {category}: {sorted_niches[:n]}") # DEBUG

    filtered_data = trends_data[top_niches]
    print("Filtering completed.") # DEBUG
    return filtered_data

def get_growth_rate(series, window=5):
    print(f"Calculating growth rate for series: {series.name} with window={window}") # DEBUG

    epsilon = 1e-10  # small constant to avoid division by zero
    shifted = series.shift(periods=window).replace(0, epsilon)
    print(f"Shifted series: {shifted}") # DEBUG

    growth_rate = series / shifted - 1
    print(f"Calculated growth rate: {growth_rate}") # DEBUG

    final_growth_rate = growth_rate.iloc[-1]
    print(f"Final growth rate: {final_growth_rate}") # DEBUG
    
    return final_growth_rate



def is_significantly_growing(series, threshold_std=1):
    print(f"Checking if series: {series.name} is significantly growing with threshold_std={threshold_std}") # DEBUG

    growth_rates = series.pct_change().dropna()
    print(f"Calculated growth rates: {growth_rates}") # DEBUG

    threshold = growth_rates.mean() + threshold_std * growth_rates.std()
    print(f"Calculated threshold: {threshold}") # DEBUG

    final_growth_rate = get_growth_rate(series)
    print(f"Final growth rate: {final_growth_rate}") # DEBUG

    is_growing = final_growth_rate > threshold
    print(f"Is the series significantly growing?: {is_growing}") # DEBUG
    
    return is_growing


def get_niche_score(niche, trends_data):
    print(f"Calculating niche score for: {niche}") # DEBUG

    total_interest = trends_data[niche].sum()
    print(f"Total interest for {niche}: {total_interest}") # DEBUG

    recent_growth = get_growth_rate(trends_data[niche])
    print(f"Recent growth for {niche}: {recent_growth}") # DEBUG

    trend_slope = get_trend_slope(trends_data[niche])
    print(f"Trend slope for {niche}: {trend_slope}") # DEBUG

    niche_score = total_interest + recent_growth + trend_slope
    print(f"Niche score for {niche}: {niche_score}") # DEBUG

    return niche_score


def get_top_niches(trends_data, n=3):
    print("Calculating top niches...") # DEBUG

    # Get the sum of the interest scores for each niche over the entire timeframe
    niche_scores = {niche: get_niche_score(niche, trends_data) for niche in trends_data.columns}
    print(f"Niche scores: {niche_scores}") # DEBUG

    # Sort the niches by their interest scores in descending order
    sorted_niches = sorted(niche_scores, key=niche_scores.get, reverse=True)
    print(f"Sorted niches: {sorted_niches}") # DEBUG

    # Get the top n niches
    top_niches = sorted_niches[:n]
    print(f"Top {n} niches: {top_niches}") # DEBUG

    return top_niches


def get_growing_trends(trends_data, threshold=1.1):
    print("Identifying growing trends...") # DEBUG
    growing_trends = []
    for column in trends_data.columns:
        trend_values = trends_data[column].values
        with np.errstate(invalid='ignore'):
            is_growing = (len(trend_values) > 1 and not (np.isnan(trend_values[-1]) or np.isnan(trend_values[-2])) and trend_values[-2] != 0 and trend_values[-1] / trend_values[-2] >= threshold)

        if is_growing:
            growing_trends.append(column)
            print(f"Growing trend found: {column}") # DEBUG

    print(f"Total growing trends identified: {len(growing_trends)}") # DEBUG
    return growing_trends

    
def get_trend_slope(series):
    y = series.values.reshape(-1, 1)
    X = np.array(range(len(series))).reshape(-1, 1)
    model = LinearRegression()
    model.fit(X, y)
    slope = model.coef_[0][0]
    print(f"Series: {series.name}, Slope: {slope}")  # DEBUG
    return slope


def main(niches, category, region='', model_choice='gpt-4', timeframe='today 12-m'):
    print(f"Starting main function with niches: {niches}, category: {category}, region: {region}, model_choice: {model_choice}")  # DEBUG

    # Initialize ideas_list
    ideas_list = []

    # Fetch Google Trends data for the niches and category
    print("Fetching Google Trends data...")  # DEBUG
    trends_data = get_trends_data(niches, category=category, region=region, timeframe=timeframe)

    # Get growing trends
    print("Getting growing trends...")  # DEBUG
    growing_trends = get_growing_trends(trends_data)

    # Get top 3 trending niches
    print("Getting top 3 trending niches...")  # DEBUG
    top_niches = get_top_niches(trends_data)

    # Filter out only the most profitable and least competitive niches
    print("Filtering niches...")  # DEBUG
    filtered_trends_data = filter_niches(trends_data)

    # Get top niches from filtered data
    print("Getting top niches from filtered data...")  # DEBUG
    top_filtered_niches = get_top_niches(filtered_trends_data)

    # Generate creative t-shirt ideas for the top niches
    for niche in top_filtered_niches:
        if ':' in niche:
            niche_name = niche.split(':')[1]
        else:
            niche_name = niche

        print(f"Generating creative t-shirt ideas for niche: {niche_name}")  # DEBUG
        prompt = openai_api.generate_prompt(niche_name, category, trends_data)
        ideas = openai_api.generate_ideas(prompt, niche, model=model_choice, n=1)
        
        ideas_list.append({"niche": niche_name, "ideas": ideas})

    print("Converting filtered trends data to a list of dictionaries...")  # DEBUG
    filtered_trends_list = filtered_trends_data.reset_index().rename(columns={"date": "Date"}).to_dict(orient="records")

    print("Preparing result...")  # DEBUG
    if ideas_list:
        return {"ideas_list": ideas_list, "trends_data": filtered_trends_list, "growing_trends": growing_trends}
    else:
        return {"ideas_list": [], "trends_data": [], "growing_trends": []}


