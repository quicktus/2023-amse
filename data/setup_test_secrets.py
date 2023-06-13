# This script is used to set up the secrets in the test environment of automated gh actions.

import os
import sys

def main():
    # kaggle
    KAGGLE_KEY = sys.argv[1]
    KAGGLE_USERNAME = sys.argv[2]

    kaggle_str = '{"username":"' + KAGGLE_USERNAME + '","key":"' + KAGGLE_KEY + '"}'
    os.makedirs("/home/runner/.kaggle", exist_ok=True)
    with open("/home/runner/.kaggle/kaggle.json", "w") as file:
        file.write(kaggle_str)

    # spotify
    SPOTIFY_CLIENT_ID = sys.argv[3]
    SPOTIFY_CLIENT_SECRET = sys.argv[4]

    spotify_str = f"{SPOTIFY_CLIENT_ID}\n{SPOTIFY_CLIENT_SECRET}\n"
    with open("./data/spotify_credentials.txt", "w") as file:
        file.write(spotify_str)

if __name__ == "__main__":
    main()
