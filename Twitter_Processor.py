import pandas as pd
import os
import subprocess
#import preprocessor as p
import re
import sys, getopt
import argparse
import os.path

try:
    import preprocessor as p
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", 'tweet-preprocessor'])
finally:
    import preprocessor as p

subprocess.call(['pip', 'install', 'wget'])
import wget

parser = argparse.ArgumentParser(description='Tweet Processor Script', formatter_class=argparse.MetavarTypeHelpFormatter)
parser.add_argument('-m', '--mode', type=int, help='mode', default = 0 )
parser.add_argument('-i', '--ifile', type=str, help='input file (optional)', default=None)
parser.add_argument('-o', '--ofile', type=str, help='output file', required= True)

args = parser.parse_args()
p.set_options(p.OPT.URL, p.OPT.EMOJI, p.OPT.HASHTAG, p.OPT.RESERVED, p.OPT.SMILEY, p.OPT.MENTION)
url = 'https://raw.githubusercontent.com/camaro1200/Tweet_Processing/main/data_elonmusk.csv'

def clean_mode1(df):
    """
        - deltes all tweets with hastags
        - removes hashtags/mentions/reserved words/Emojis/Smileys
    """
    
    for i,v in enumerate(df['Tweet']):
        parsed_tweet = p.parse(v)
        if parsed_tweet.hashtags != None:
            df = df.drop(i)
        else:
            df.loc[i,'Cleaned_Tweet'] = p.clean(v)
     
    return df


class CreateDataset():
    def __init__(self, mode, ifile, ofile):
        if ifile == None:
            self.ifile = wget.download(url)
        else:
            self.ifile = ifile
        self.mode = mode
        self.ofile = ofile
    
    def load_dataset(self):
        if os.path.isfile(self.ifile) == False:
            print("no such input file found")
            sys.exit(2)
        
        df = pd.read_csv(self.ifile, encoding='windows-1252')
        
        if self.mode == 0:
            df.to_csv(self.ofile, index=False)
        elif self.mode == 1:
            df = clean_mode1(df)
            df.to_csv(self.ofile, index=False)
        else:
            print ("no such mode found, please enter valid mode")
            sys.exit(2)
        

def main():
    dataset = CreateDataset(mode=args.mode, ifile=args.ifile, ofile= args.ofile)
    dataset.load_dataset()
    
    print("\nprocess finished")
      
    
if __name__ == "__main__":
    main()
