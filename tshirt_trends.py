import pandas as pd
from pytrends.request import TrendReq
from pytrends.exceptions import TooManyRequestsError
import random
import time
import numpy as np
from sklearn.linear_model import LinearRegression
from openai_api import IdeaGenerator
from config import MML_MODEL_FILE, PROMPT_FILE, OPENAI_API_KEY

# Function to fetch Google Trends data
def get_trends_data(keywords, category, timeframe='today 12-m', region='US'):
    pytrends = TrendReq(hl='en-GB', tz=360)
    backoff_time = 5

    while True:
        try:
            print(f"Fetching trends data for keywords: {keywords}, category: {category}, timeframe: {timeframe}, region: {region}")
            pytrends.build_payload(keywords, cat=category, timeframe=timeframe, geo=region, gprop='froogle')
            data = pytrends.interest_over_time()

            # Get related queries
            print("Fetching related queries...")
            related_queries = pytrends.related_queries()
            related_queries_list = []

            for keyword, related_data in related_queries.items():
                top_related = related_data['top']
                if top_related is not None:
                    related_queries_list.extend(list(top_related['query']))
            print(f"Related queries: {related_queries_list}")

            # Get suggestions for related queries
            print("Fetching suggestions for related queries...")
            niches = [f"{keyword}:{pytrends.suggestions(keyword)[0]['type']}" if pytrends.suggestions(keyword) else f"{keyword}:" for keyword in related_queries_list]
            niches += [''] * (2 - len(niches))
            print(f"Suggestions for related queries: {niches}")

            # Combine the original data with the data for the related queries
            print("Combining the original data with the data for the related queries...")
            related_data = pd.DataFrame(columns=related_queries_list, index=data.index)
            for keyword in related_queries_list:
                related_data[keyword] = pytrends.get_historical_interest([keyword], year_start=2022, month_start=1, day_start=1, hour_start=0, year_end=2022, month_end=2, day_end=1, hour_end=0, cat=category, geo=region, gprop='', sleep=0)[keyword]
            combined_data = pd.concat([data, related_data], axis=1)
            print("Combined data ready.")

            # Return the data
            return combined_data
        except TooManyRequestsError:
            delay = random.uniform(backoff_time, backoff_time * 1.5)
            print(f"Too many requests, waiting for {delay} seconds before retrying...")
            time.sleep(delay)
            backoff_time *= 1.5
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            print("Retrying...")
            backoff_time *= 1.5

def filter_niches(trends_data, n=3):
    print(f"Filtering niches from trends data with n={n}...")

    niche_means = trends_data.mean().to_dict()
    niche_means.pop('isPartial', None)
    print(f"Calculated means for niches: {niche_means}")

    category_means = {}
    for niche in niche_means:
        category = niche.split(':')[0]
        if category in category_means:
            category_means[category].append(niche_means[niche])
        else:
            category_means[category] = [niche_means[niche]]

    category_means = {k: sum(v)/len(v) for k, v in category_means.items()}
    print(f"Calculated means for categories: {category_means}")

    niche_trends = {niche: get_trend_slope(trends_data[niche]) for niche in niche_means}
    print(f"Calculated trends for niches: {niche_trends}")

    sorted_categories = sorted(category_means.keys(), key=lambda x: category_means[x], reverse=True)
    print(f"Sorted categories: {sorted_categories}")

    top_niches = []
    for category in sorted_categories:
        category_niches = [niche for niche in niche_means if niche.split(':')[0] == category]
        sorted_niches = sorted(category_niches, key=lambda x: niche_means[x], reverse=True)
        top_niches += sorted_niches[:n]
        print(f"Top {n} niches for category {category}: {sorted_niches[:n]}")

    filtered_data = trends_data[top_niches]
    print("Filtering completed.")
    return filtered_data

def get_growth_rate(series, window=5):
    print(f"Calculating growth rate for series: {series.name} with window={window}")

    epsilon = 1e-10
    shifted = series.shift(periods=window).replace(0, epsilon)
    print(f"Shifted series: {shifted}")

    growth_rate = series / shifted - 1
    print(f"Calculated growth rate: {growth_rate}")

    final_growth_rate = growth_rate.iloc[-1]
    print(f"Final growth rate: {final_growth_rate}")

    return final_growth_rate

def is_significantly_growing(series, threshold_std=1):
    print(f"Checking if series: {series.name} is significantly growing with threshold_std={threshold_std}")

    growth_rates = series.pct_change().dropna()
    print(f"Calculated growth rates: {growth_rates}")

    threshold = growth_rates.mean() + threshold_std * growth_rates.std()
    print(f"Calculated threshold: {threshold}")

    final_growth_rate = get_growth_rate(series)
    print(f"Final growth rate: {final_growth_rate}")

    is_growing = final_growth_rate > threshold
    print(f"Is the series significantly growing?: {is_growing}")

    return is_growing

def get_niche_score(niche, trends_data):
    print(f"Calculating niche score for: {niche}")

    total_interest = trends_data[niche].sum()
    print(f"Total interest for {niche}: {total_interest}")

    recent_growth = get_growth_rate(trends_data[niche])
    print(f"Recent growth for {niche}: {recent_growth}")

    trend_slope = get_trend_slope(trends_data[niche])
    print(f"Trend slope for {niche}: {trend_slope}")

    niche_score = total_interest + recent_growth + trend_slope
    print(f"Niche score for {niche}: {niche_score}")

    return niche_score

def get_top_niches(trends_data, n=3):
    print("Calculating top niches...")

    niche_scores = {niche: get_niche_score(niche, trends_data) for niche in trends_data.columns}
    print(f"Niche scores: {niche_scores}")

    sorted_niches = sorted(niche_scores, key=niche_scores.get, reverse=True)
    print(f"Sorted niches: {sorted_niches}")

    top_niches = sorted_niches[:n]
    print(f"Top {n} niches: {top_niches}")

    return top_niches

def get_growing_trends(trends_data, threshold=1.1):
    print("Identifying growing trends...")
    growing_trends = []
    for column in trends_data.columns:
        trend_values = trends_data[column].values
        with np.errstate(invalid='ignore'):
            is_growing = (len(trend_values) > 1 and not (np.isnan(trend_values[-1]) or np.isnan(trend_values[-2])) and trend_values[-2] != 0 and trend_values[-1] / trend_values[-2] >= threshold)

        if is_growing:
            growing_trends.append(column)
            print(f"Growing trend found: {column}")

    print(f"Total growing trends identified: {len(growing_trends)}")
    return growing_trends

def get_trend_slope(series):
    y = series.values.reshape(-1, 1)
    X = np.array(range(len(series))).reshape(-1, 1)
    model = LinearRegression()
    model.fit(X, y)
    slope = model.coef_[0][0]
    print(f"Series: {series.name}, Slope: {slope}")
    return slope

# Instantiate IdeaGenerator with your paths
idea_gen = IdeaGenerator(OPENAI_API_KEY, MML_MODEL_FILE, PROMPT_FILE)
def main(niches, category, region=None, model_choice='gpt-4', timeframe='today 12-m'):
    print(f"Starting main function with niches: {niches}, category: {category}, region: {region}, model_choice: {model_choice}")

    # Fetch Google Trends data for the niches and category
    print("Fetching Google Trends data...")
    trends_data = get_trends_data(niches, category=category, region=region, timeframe=timeframe)

    # Get growing trends
    print("Getting growing trends...")
    growing_trends = get_growing_trends(trends_data)

    # Get top 3 trending niches
    print("Getting top 3 trending niches...")
    top_niches = get_top_niches(trends_data)

    # Filter out only the most profitable and least competitive niches
    print("Filtering niches...")
    filtered_trends_data = filter_niches(trends_data)

    # Get top niches from filtered data
    print("Getting top niches from filtered data...")
    top_filtered_niches = get_top_niches(filtered_trends_data)

    # Initialize ideas_list
    ideas_list = []

    # Generating creative t-shirt ideas
    for niche in niches:
        if ":" in niche:
            niche_name = niche.split(':')[1]
        else:
            niche_name = niche

        print(f"Generating creative t-shirt ideas for niche: {niche_name}")

        # generate ideas
        ideas = idea_gen.generate_ideas(niche_name, category, trends_data, model=model_choice, n=10)

        ideas_list.append({"niche": niche_name, "ideas": ideas})

    # Convert filtered trends data to a list of dictionaries
    filtered_trends_list = filtered_trends_data.reset_index().rename(columns={"date": "Date"}).to_dict(orient="records")

    print("Preparing result...")
    if niches:
        return {"ideas_list": ideas_list, "trends_data": filtered_trends_list, "growing_trends": growing_trends}
    else:
        return {"ideas_list": [], "trends_data": [], "growing_trends": []}

