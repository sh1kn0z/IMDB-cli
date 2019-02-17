from bs4 import BeautifulSoup
from tabulate import tabulate
from CONST import *
import pandas as pd
import requests
import re


class IMDB:

    def __init__(self):
        self.titles = []
        self.years = []
        self.genres = []
        self.runtimes = []
        self.ratings = []
        self.summaries = []

    @staticmethod
    def build_query_string(title, title_type=None):
        query_string = URL + '+'.join(title)
        if title_type:
            title_type = ','.join(title_type)
            query_string += f'&title_type={title_type}'
        return query_string

    @staticmethod
    def execute_query(query_string):
        """
        sends GET request to given url with querystring and gets the response HTML (string)
        :param query_string: the url
        :return string: the string of the responses HTML
        """
        response = requests.get(query_string, HEADERS)
        return response.content.decode('utf-8')

    @staticmethod
    def splitter(num, text):
        """
        splits the text to {num} words in each line
        :param int num: the number of words in each line
        :param string text: the whole text
        :return string:
        """
        pieces = text.split()
        lines = [' '.join(pieces[i:i + num]) for i in range(0, len(pieces), num)]
        return '\n'.join(lines)

    def extract_data(self, search_result):
        """
        this function extracts the data from the given html argument
        :param string search_result: given html file as string
        """
        soup = BeautifulSoup(search_result, 'html.parser')

        # find all movies according to search result and loop through them
        movies = soup.find_all('div', class_='lister-item mode-advanced')
        for movie in movies:
            h3 = movie.find('h3', class_='lister-item-header')

            # get the title of the movie
            title = IMDB.splitter(6, h3.a.text)
            self.titles.append(title)

            # get the year of the movie
            year_type = h3.find('span', class_='lister-item-year text-muted unbold').text
            year_search = re.search(YEAR_REGEX, year_type)
            year = year_search.group() if year_search else '-'
            self.years.append(year)

            # get the genre of the movie
            find_genre = movie.find('span', class_='genre')
            genre = find_genre.text.strip(' \t\n\r') if find_genre else '-'
            genre = IMDB.splitter(2, genre)
            self.genres.append(genre)

            # get the runtime of the movie
            find_movie_length = movie.find('span', class_='runtime')
            runtime = find_movie_length.text if find_movie_length else '-'
            self.runtimes.append(runtime)

            # get the rating of the movie
            find_rating = movie.find('div', class_='inline-block ratings-imdb-rating')
            rating = find_rating['data-value'] if find_rating else '-'
            self.ratings.append(rating)

            # get the summary of the movie
            summary = IMDB.splitter(8, movie.find_all('p', class_='text-muted')[1].text)
            if summary == 'Add a Plot':
                summary = 'Review is not available'
            self.summaries.append(summary)

    def build_table(self):
        """
        this function builds the output table
        """
        pd.set_option('display.max_rows', 500)
        pd.set_option('display.max_columns', 500)
        pd.set_option('display.width', 1000)

        df = pd.DataFrame({
            'Title': self.titles,
            'Year': self.years,
            'Genre': self.genres,
            'Length': self.runtimes,
            'Rating': self.ratings,
            'Summary': self.summaries
        })

        print(tabulate(df.head(10), showindex=False, headers=df.columns, tablefmt='fancy_grid'))
