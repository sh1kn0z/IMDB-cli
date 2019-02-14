import requests
from bs4 import BeautifulSoup
import argparse
import pandas as pd
import re
from tabulate import tabulate

titles = []
years = []
genres = []
runtimes = []
ratings = []
summaries = []
YEAR = re.compile(r'[1|2][9|0]\d\d')

def build_url(args):
    url = 'https://www.imdb.com/search/title?title='
    title = '+'.join(args.title)
    url += title
    if args.title_type:
        title_type = ','.join(args.title_type)
        url += f"&title_type={title_type}"
    # print(url)
    return url

def execute_query(url):
    headers = {"Accept-Language": "en-US, en;q=0.5"}
    response = requests.get(url, headers)
    return response.content.decode('utf-8')

def extract_data(search_result):
    soup = BeautifulSoup(search_result, 'html.parser')
    movies = soup.find_all('div', class_='lister-item mode-advanced')
    for movie in movies:
        h3 = movie.find('h3', class_='lister-item-header')

        title = splitter(6, h3.a.text)

        year_type = h3.find('span', class_='lister-item-year text-muted unbold').text
        year_search = re.search(YEAR, year_type)
        year = year_search.group() if year_search else '-'

        find_genre = movie.find('span', class_='genre')
        genre = find_genre.text.strip(' \t\n\r') if find_genre else '-'
        genre = splitter(2, genre)

        find_movie_length = movie.find('span', class_='runtime')
        runtime = find_movie_length.text if find_movie_length else '-'

        find_rating = movie.find('div', class_='inline-block ratings-imdb-rating')
        rating = find_rating['data-value'] if find_rating else ''

        summary = splitter(8, movie.find_all('p', class_='text-muted')[1].text)
        if summary == 'Add a Plot':
            summary = 'Review is not available'

        titles.append(title)
        years.append(year)
        genres.append(genre)
        runtimes.append(runtime)
        ratings.append(rating)
        summaries.append(summary)

def build_table():
    # pd.set_option('display.height', 1000)
    pd.set_option('display.max_rows', 500)
    pd.set_option('display.max_columns', 500)
    pd.set_option('display.width', 1000)

    df = pd.DataFrame({
        'Title': titles,
        'Year': years,
        'Genre': genres,
        'Length': runtimes,
        'Rating': ratings,
        'Summary': summaries
    })

    # df.style.set_table_styles([dict(selector="td", props=[('max-width', '50px')])])
    # print(df.head(10))
    print(tabulate(df.head(10), showindex=False, headers=df.columns, tablefmt='fancy_grid'))

    # print(test_df.info())
    # print(df.head(10))

def splitter(n, s):
    pieces = s.split()
    pieces2 = [" ".join(pieces[i:i+n]) for i in range(0, len(pieces), n)]
    return "\n".join(pieces2)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--title', nargs='+', type=str, required=True, help='title of the movie')
    parser.add_argument(
        '--title_type',
        type=str,
        nargs='+',
        choices=[
            'feature', 'tv_movie', 'tv_series', 'tv_episode', 'tv_special', 'tv_miniseries', 'documentary',
            'video_game', 'short', 'video', 'tv_short'
        ],
        help='title type of the movie'
    )
    args = parser.parse_args()
    url = build_url(args)
    search_result = execute_query(url)
    extract_data(search_result)
    build_table()

if __name__ == '__main__':
    main()