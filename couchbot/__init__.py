import argparse
import re
import requests
from slackclient import SlackClient


def parse_args():
    global bot_token, couch_key, couch_url
    parser = argparse.ArgumentParser()
    parser.add_argument("bot_token", help="Slack bot API token",
                        type=str)
    parser.add_argument("couch_key", help="Couch Potato API key",
                        type=str)
    parser.add_argument("couch_url", help="Couch Potato server URL",
                        type=str)

    args = parser.parse_args()
    bot_token = args.bot_token
    couch_key = args.couch_key
    couch_url = args.couch_url


def send_message_to_channel(msg, channel, sc):
    sc.rtm_send_message(channel, msg)


def prepare_couch_data(messages, bot_mention):
    messenger_data = {'imdb_ids': []}
    for msg in messages:
        if 'subtype' in msg:
            continue

        if msg.get('type') == "message":
            raw = msg['text']
            messenger_data['user'] = '<@{}>'.format(msg['user'])
            messenger_data['channel'] = msg['channel']

            if bot_mention in raw:
                ids = set(re.findall(r'imdb.com/title/(.+?)/', raw))
                messenger_data['imdb_ids'] = ids

    return messenger_data


def tell_couch_potato(slack_data, sc):
    for imdb_id in slack_data['imdb_ids']:
        post_data = {
            'identifier': imdb_id
        }
        url = '{}api/{}/'.format(couch_url, couch_key)
        url = '{}{}'.format(url, 'movie.add/')
        response = requests.post(url, post_data).json()
        if response['success']:
            msg = '{} added movie: {}'.format(
                slack_data['user'],
                response['movie']['info']['original_title']
            )
            send_message_to_channel(msg, slack_data['channel'], sc)
        else:
            link = 'http://www.imdb.com/title/{}'.format(imdb_id)
            send_message_to_channel(
                'Failed to add movie {}'.format(link),
                slack_data['channel'],
                sc
            )


def start():
    global bot_token
    sc = SlackClient(bot_token)

    if sc.rtm_connect():
        bot_id = sc.server.users[0].id
        bot_mention = '<@{}>'.format(bot_id)
        while True:
            rtm = sc.rtm_read()
            if len(rtm) > 0:
                slack_data = prepare_couch_data(rtm, bot_mention)
                if len(slack_data['imdb_ids']) > 0:
                    tell_couch_potato(slack_data, sc)
    else:
        print("Connection Failed, invalid token")


def main():
    parse_args()
    start()


if __name__ == "__main__":
    main()
