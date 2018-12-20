import os
import json
import re
import pickle
import itertools

# To change accordingly
AUTHOR = 'Joshia Seam'
ROOT = './facebook-joshiaseam'

comments = os.path.join(ROOT, 'comments')
groups = os.path.join(ROOT, 'groups')
messages = os.path.join(ROOT, 'messages')
posts = os.path.join(ROOT, 'posts')


def get_files(directory, filetype='.json'):
    """
    Returns the files in the directory

    Args:
        directory: String, input the directory we traverse
        filetype: String, input the filetype we look for

    Returns:
        List of Strings, returns the list of files found
    """
    ls = []
    for subdir, dirs, files in os.walk(directory):
        for f in files:
            if f.endswith('.json'):
                # We are only concerned about json files
                ls.append(os.path.join(subdir, f))
    return ls


def get_comments():
    """
    Get user comments
    We are only concerned about /comments/comments.json

    Returns:
        list: List of Strings, returns list of comments
    """
    f = os.path.join(comments, 'comments.json')

    try:
        with open(f) as jsonfile:
            data = json.load(jsonfile)

    except FileNotFoundError:
        print("{} is not found, cannot extract comments".format(f))
        return

    ls = []
    for c in data['comments']:
        for d in c['data']:
            try:
                ls.append(d['comment']['comment'])

            except KeyError:
                # If there is a key error we continue
                continue
    return ls


def get_posts():
    """
    Get user posts
    We are only concerned about /posts/your_posts.json

    Returns:
        list: List of Strings, returns list of posts
    """
    f = os.path.join(posts, 'your_posts.json')

    try:
        with open(f) as jsonfile:
            data = json.load(jsonfile)
    except FileNotFoundError:
        print("{} is not found, cannot extract posts.".format(f))
        return

    ls = []
    for c in data['status_updates']:
        try:
            for d in c['data']:
                ls.append(d['post'])

        except KeyError:
            # If there is a key error we continue
            continue

    return ls


def get_messages():
    """
    Get user messages
    We are only concerned about messages when sender_name == author

    Returns:
        list: List of Strings, returns list of messages
    """
    files = get_files(messages)

    ls = []

    for f in files:
        try:
            with open(f) as jsonfile:
                data = json.load(jsonfile)
        except FileNotFoundError:
            print("{} is not found, skipping."format(f))
            continue

        try:
            for message in data['messages']:
                if message['sender_name'] != AUTHOR:
                    continue
                elif message['content'][:9] == "Say hi to":
                    continue
                elif message['content'] == \
                        "You are now connected on Messenger.":
                    continue
                elif message['content'] == \
                        "You sent an attachment.":
                    continue
                elif message['content'] == \
                        "You sent a photo.":
                    continue
                elif message['content'] == \
                        "You sent a link.":
                    continue
                elif message['content'][-20:] == \
                        "waved at each other!":
                    continue
                else:
                    ls.append(message['content'])

        except KeyError:
            continue

    return ls


def get_groups():
    """
    Get user posts in groups
    We are only concerned about comments when author = AUTHOR

    Returns:
        list: List of Strings, returns list of comments
    """
    f = os.path.join(groups, 'your_posts_and_comments_in_groups.json')

    try:
        with open(f) as jsonfile:
            data = json.load(jsonfile)
    except FileNotFoundError:
        print("{} is not found. Cannot get group data".format(f))
        return

    ls = []
    for post in data['group_posts']:
        try:
            for d in post['data']:
                # the comments exists in two forms
                try:
                    if d['comment']:
                        ls.append(d['comment']['comment'])
               except KeyError:
                    pass

                try:
                    if d['comments']:
                        for x in d['comments']:
                            if x['author'] == AUTHOR:
                                ls.append(x['comment'])
                except KeyError:
                    pass
        except KeyError:
            pass

    return ls


def get_all(remove_url=True, only_ascii=True, separate_newline=True):
    """
    Returns a list of all the string data

    Args:
        remove_url (bool): If true remove lines that contain url
        only_ascii (bool): If true remove non-ascii character

    Returns:
        list: List of Strings, returns list of cleaned string

    """
    total = get_comments() + get_posts() + get_messages() + get_groups()

    if not remove_url and not only_ascii:
        return total

    url = \
        re.compile('(n)?http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]\
                   |(?:%[0-9a-fA-F][0-9a-fA-F]))+')

    not_ascii = re.compile('[^\x00-\x7f]|[\d()]| - .+\b(?=\n)')

    new_total = []

    for line in total:
        # flag
        to_append = True

        if remove_url:
            if url.search(line):
                to_append = False

        if to_append:
            if only_ascii:
                # We substitute non ascii with blanks
                line = not_ascii.sub(r'', line)

            # final processing step
            # omit empty lines
            if line.strip() != '':
                # Converts to lower case
                new_line = line.lower()
                new_line = new_line.replace('\n', ' ')
                new_total.append(new_line)

    return new_total


if __name__ == "__main__":
    string = get_all()
    print(string)
    # save pickle
    pickle.dump(string, open("data.pkl", "wb"))
