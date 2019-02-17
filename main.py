import argparse
from IMDB import IMDB


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--title', nargs='+', type=str, required=True, help='Title of the movie')
    parser.add_argument(
        '--title_type',
        type=str,
        nargs='+',
        choices=[
            'feature', 'tv_movie', 'tv_series', 'tv_episode', 'tv_special', 'tv_miniseries', 'documentary',
            'video_game', 'short', 'video', 'tv_short'
        ],
        help='The Title type of the movie'
    )
    args = parser.parse_args()

    imdb = IMDB()
    if args.title_type:
        IMDB.title_type = args.title_type

    url = imdb.build_query_string(args.title, args.title_type)
    search_result = imdb.execute_query(url)
    imdb.extract_data(search_result)
    imdb.build_table()


if __name__ == '__main__':
    main()
