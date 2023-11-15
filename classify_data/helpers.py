import random

import nltk
import numpy as np
import pandas as pd
from nltk.corpus import stopwords as sw
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer

nltk.download('stopwords')
nltk.download('wordnet')


def clean_text(text: pd.DataFrame) -> pd.DataFrame:
    """
    Function that cleans the text by removing stopwords and lemmatizing the words
    """
    stopwords = sw.words('english')
    lemmatizer = WordNetLemmatizer()

    text = text.str.lower()
    text = text.str.replace('[^\w\s]', '')
    text = text.str.replace('\d+', '')
    text = text.apply(lambda x: ' '.join([lemmatizer.lemmatize(word) for word in x.split() if word not in stopwords]))
    return text

def transform_data(dataset):
    """Converts the dataset into a format that can be used by the classifier"""
    result = pd.DataFrame(index=dataset.user.unique())
    result['bot'] = dataset.groupby('user').bot.max()
    result['bot_in_name'] = result.index.map(lambda x: 'bot' in x.lower())

    dataset['bot_in_comment'] = dataset.comment.str.lower().str.contains('bot')
    result['bot_in_comment'] = dataset.groupby('user').bot_in_comment.mean() > 0.5

    dataset['day'] = dataset.timestamp.dt.day
    dataset['hour'] = dataset.timestamp.dt.hour
    result['changes_per_day'] = dataset.groupby(['day', 'user']).day.count().groupby('user').mean()
    result['changes_per_day_min'] = dataset.groupby(['day', 'user']).day.count().groupby('user').min()
    result['changes_per_day_max'] = dataset.groupby(['day', 'user']).day.count().groupby('user').max()

    result['changes_per_hour'] = dataset.groupby(['hour', 'day', 'user']).hour.count().groupby('user').mean()
    result['changes_per_hour_min'] = dataset.groupby(['hour', 'day', 'user']).hour.count().groupby('user').min()
    result['changes_per_hour_max'] = dataset.groupby(['hour', 'day', 'user']).hour.count().groupby('user').max()

    dataset['edit_length'] = dataset.length.apply(lambda x: abs(x['old'] - x['new']) if x else 0)
    result['edit_length_mean'] = dataset.groupby('user').edit_length.mean()
    result['edit_length_min'] = dataset.groupby('user').edit_length.min()
    result['edit_length_max'] = dataset.groupby('user').edit_length.max()

    result['pages_edited'] = dataset.groupby('user').title.nunique()
    result['pages_edited_per_day'] = dataset.groupby(['day', 'user']).title.nunique().groupby('user').mean()
    result['pages_edited_per_day_min'] = dataset.groupby(['day', 'user']).title.nunique().groupby('user').min()
    result['pages_edited_per_day_max'] = dataset.groupby(['day', 'user']).title.nunique().groupby('user').max()

    result['pages_edited_per_hour'] = dataset.groupby(['hour', 'day', 'user']).title.nunique().groupby('user').mean()
    result['pages_edited_per_hour_min'] = dataset.groupby(['hour', 'day', 'user']).title.nunique().groupby('user').min()
    result['pages_edited_per_hour_max'] = dataset.groupby(['hour', 'day', 'user']).title.nunique().groupby('user').max()

    tfidf = TfidfVectorizer(max_features=10)
    tfidf.fit(clean_text(dataset.comment))
    tfidf_columns = [f'tfidf_{feature}' for feature in tfidf.get_feature_names_out()]
    tfidf_data = pd.DataFrame(tfidf.transform(dataset.comment).toarray(), columns=tfidf_columns).fillna(0)
    dataset = pd.concat([dataset, tfidf_data], axis=1)
    result[tfidf_columns] = dataset.groupby('user')[tfidf_columns].mean()

    return result


def set_seed(seed):
    random.seed(seed)
    np.random.seed(seed)
