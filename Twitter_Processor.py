import os
import subprocess
#import preprocessor as p
#import pandas as pd
import re
import sys, getopt
import argparse
import os.path

try:
    import preprocessor as p
    import wget
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", 'tweet-preprocessor'])
    subprocess.call(['pip', 'install', 'wget'])
    subprocess.call(['pip', 'install', 'pandas'])
    subprocess.call(['pip', 'install', 'nltk'])
finally:
    import preprocessor as p
    import wget
    import pandas as pd
    import nltk

# subprocess.call(['pip', 'install', 'wget'])
# import wget

# subprocess.call(['pip', 'install', 'pandas'])
# import pandas as pd

# subprocess.call(['pip', 'install', 'nltk'])
# import nltk

parser = argparse.ArgumentParser(description='Tweet Processor Script', formatter_class=argparse.MetavarTypeHelpFormatter)
parser.add_argument('-m', '--mode', type=int, help='mode', default = 0 )
parser.add_argument('-o', '--ofile', type=str, help='output file', required=True)
parser.add_argument('-l', '--ltweet', type=int, help='Min Lenght of Tweet', default=0)

args = parser.parse_args()
p.set_options(p.OPT.URL, p.OPT.EMOJI, p.OPT.HASHTAG, p.OPT.RESERVED, p.OPT.SMILEY, p.OPT.MENTION)
url = 'https://raw.githubusercontent.com/camaro1200/Tweet_Processing/main/data_elonmusk.csv'


def clean_mode1(df, min_len):
    """
        - deltes all tweets with hastags
        - removes hashtags/mentions/reserved words/Emojis/Smileys
        - deletes all tweets with min lenght
    """
    
    for i,v in enumerate(df['Tweet']):
        parsed_tweet = p.parse(v)
        if parsed_tweet.hashtags != None:
            df = df.drop(i)
        else:
            cleaned_tweet = p.clean(v)
            tokens = nltk.word_tokenize(cleaned_tweet)
            if len(tokens) < min_len:
                df = df.drop(i)
            else:
                df.loc[i,'Cleaned_Tweet'] = cleaned_tweet
        
    return df


class CreateDataset():
    def __init__(self, mode, ltweet, ofile):
        self.ltweet = ltweet
        self.ifile = wget.download(url)
        self.mode = mode
        self.ofile = ofile
    
    def load_dataset(self):
        
        df = pd.read_csv(self.ifile, encoding='windows-1252')
        df = df.drop(['Time', 'Retweet from', 'User'], axis=1)
        
        if self.mode == 0:
            print("no changes made")
        elif self.mode == 1:
            df = clean_mode1(df, self.ltweet)
        else:
            print ("no such mode found, please enter valid mode")
            sys.exit(2)
        
        df.to_csv(self.ofile, index=False)
        os.remove(self.ifile)
        

def main():
    dataset = CreateDataset(mode=args.mode, ltweet=args.ltweet, ofile= args.ofile)
    dataset.load_dataset()
    
    print("\nprocess finished")
      
    
if __name__ == "__main__":
    main()
