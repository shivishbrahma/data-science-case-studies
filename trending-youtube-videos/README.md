# Youtube Dataset Analysis

## Use Cases

Possible uses for this dataset could include:

- Sentiment analysis in a variety of forms
- Categorising YouTube videos based on their comments and statistics.
- Training ML algorithms like RNNs to generate their own YouTube comments.
- Analysing what factors affect how popular a YouTube video will be.
- Statistical analysis over time.

## Dataset Description

This dataset includes several months (and counting) of data on daily trending YouTube videos.

Data is included for the US, GB, DE, CA, and FR regions (USA, Great Britain, Germany, Canada, and France, respectively), with up to 200 listed trending videos per day.

EDIT: Now includes data from RU, MX, KR, JP and IN regions (Russia, Mexico, South Korea, Japan and India respectively) over the same time period.

Each region’s data is in a separate file. Data includes the video title, channel title, publish time, tags, views, likes and dislikes, description, and comment count.

The data also includes a `category_id` field, which varies between regions. To retrieve the categories for a specific video, find it in the associated `JSON`. One such file is included for each of the five regions in the dataset.

### Citation

Mitchell J. (November 30, 2018). Trending YouTube Video Statistics, Version 1. Retrieved September 6, 2025 from [https://www.kaggle.com/datasets/datasnaek/youtube-new/version/1](https://www.kaggle.com/datasets/datasnaek/youtube-new/version/1).

## Data Preparation

- Merge `input/youtube-new/**videos.csv` into a single dataframe (videos_df).
- Merge `input/youtube-new/**_category_id.json` into a single dataframe (categories_df).

## Data Preprocessing & Cleaning

- Extract the `country_cd` from the `filename`.
- Convert the `category_id` column into `int`.
- Convert the `trending_date` into datetime
- Drop the unnecessary columns (`filename`, `video_id`, `kind`, `etag`, `snippet_channelId`)
- Merge the `categories_df` into the `videos_df` on `category_id` and `country_cd`.
- Rename columns `snippet_title` to `category_title`, `snippet_assignable` to `category_assignable`.
- Write the cleaned dataframe to `working/videos_cleaned.csv`

## Notebooks

- [Data Ingestion](./01_processing_notebook.ipynb)
