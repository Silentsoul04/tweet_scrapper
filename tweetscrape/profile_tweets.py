import logging

from tweetscrape.tweets_scrape import TweetScrapper
from tweetscrape.search_tweets import TweetScrapperSearch

"""
Parsing with XPath 1.0 query
XPath Documentation : https://developer.mozilla.org/en-US/docs/Web/XPath
The '.' at the beginning means, that the current processing starts at the current node.
Your xpath starts with a slash '/' and is therefore absolute.
The '*' selects all element nodes descending from this current node with the @id-attribute-value or @class value'.
The '//' identifies any descendant designation element of element
"""

logger = logging.getLogger(__name__)


class TweetScrapperProfile(TweetScrapper):
    username = "5hirish"
    pages = 0

    __twitter_profile_url__ = None
    __twitter_profile_header__ = None
    __twitter_profile_params__ = None

    def __init__(self, username, pages=2, *args):
        self.username = username

        self.__twitter_profile_url__ = 'https://twitter.com/i/profiles/show/{username}/timeline/tweets' \
            .format(username=self.username)

        self.__twitter_profile_params__ = {
            'include_available_features': 1,
            'include_entities': 1,
            'include_new_items_bar': True
        }

        self.__twitter_profile_header__ = {
            'referer': 'https://twitter.com/{username}'.format(username=self.username)
        }

        super().__init__(self.__twitter_profile_url__,
                         self.__twitter_profile_header__,
                         self.__twitter_profile_params__,
                         pages, *args)

    def get_profile_tweets(self, save_output=False):
        output_file_name = '/' + self.username + '_profile'
        # Search Profile since: until: from:
        tweet_count, last_tweet_time, dump_path = self.execute_twitter_request(username=self.username,
                                                                               log_output=save_output,
                                                                               output_file=output_file_name)

        if self.pages == -1 or self.pages - 1 * 20 < tweet_count:
            ts = TweetScrapperSearch(search_from_accounts=self.username,
                                     search_from_date=TweetScrapperSearch.twitter_from_date,
                                     search_till_date=last_tweet_time)
            append_tweet_count, last_tweet_time, dump_path = ts.get_search_tweets(save_output)
            tweet_count += append_tweet_count

        return tweet_count, last_tweet_time, dump_path


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    l_ts = TweetScrapperProfile("BarackObama", -1, 'twitter.csv', 'csv')
    l_tweet_count, l_tweet_time, l_dump_path = l_ts.get_profile_tweets(True)
    # for l_tweet in l_extracted_tweets:
    #     print(str(l_tweet))
    print(l_tweet_count)
