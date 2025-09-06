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
