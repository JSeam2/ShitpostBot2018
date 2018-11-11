import os
import sys

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

def get_author_data_comments(f, author="Joshia Seam"):
    """
    Get author data in comments

    Args:
        f: String, filename
        author: String, author name

    """


if __name__ == "__main__":
    print(get_files(comments))
