# PirlaStamp-Lite

PirlaStamp-Lite is a local version of TweetStamp, designed to comply with Twitter rules and GDPR. It is important to note that putting an online version of TweetStamp could violate Twitter's policies and GDPR, so it is necessary to use PirlaStamp-Lite only at a local level and not share it on the Internet.

## Features

- Allows users to easily save tweets locally with a timestamp
- Ensures that saved tweets are compliant with Twitter rules and GDPR
- Utilizes Flask and Tweepy dependencies and MongoDB

## Installation

To download PirlaStamp-Lite, use git clone or press the download button. Dependencies include Flask and Tweepy, and you will need to have API keys which should be added to the keys file found in the keys folder. Also save the data in MongoDB to not lose it every time

## Usage

To use PirlaStamp-Lite, first launch the server with the command 'python server.py'. Then, in another window, launch 'python insert_tweet.py' followed by the URL of the tweet you want to save.

## Contributing

If you want to contribute to PirlaStamp-Lite, please open an issue or pull request.

## License

PirlaStamp-Lite is released under the MIT license. For more information, see the LICENSE file.
