# This script pulls from GitHub repository raw Prior Bank html pages that was committed by GitHub action 
# on cron time schedule. (prior_get_content_gh.py) Then it scraps information on currency rates and loads it to postgres database.
# After currency rates are loade to database, raw file is saved in compressed format to backup folder and
# then deleted from git. When all files are processed git changes are committed to GitHub. 
#
# The script has one positional parametr, specifying target postgres environment. 'dev' or 'prod' are possible values.
#
# leotepl@gmail.com
#

import git
import datetime
import glob
import os
import re
import gzip
import argparse
from ScrapCurrRatesPrior import scrapCurrRatesPrior 
from LoadDF2DB import loadDF2DB 

# parsing input arguments

parser= argparse.ArgumentParser(description='Pull front page from prior.by')
parser.add_argument('env',metavar='1',type=str,nargs='?',help='environment, prod or dev')
args=parser.parse_args()

print(parser.prog+": "+datetime.datetime.now().strftime("%Y-%m-%d, %H:%M:%S")+" started on "+args.env )

# defining consgants

rawBackupPath='/opt/CurrencyRatingAnalysis/RawFilesBackup/'  # backup folder for raw files
gitRepoPath='/opt/CurrencyRatingAnalysis/github'             # path to local git repo
timestamp_mask=re.compile('.*prior_page_(\d\d\d\d-\d\d-\d\d)_(\d\d:\d\d:\d\d)\.html')  # regex to extract time stamp from file name

# function to extract timestamp when raw file was created from file name

def file_name_timestamp(f):
    m=timestamp_mask.match(f)
    return (m.group(1)+' '+m.group(2))+'+00:00'  # timestamp on file name is in GMT

my_repo = git.Repo(gitRepoPath)  # initialize git repository object
my_repo.git.checkout('master')   # checkout master branch
my_repo.remotes.origin.pull()    # pull from github

file_list=glob.glob(gitRepoPath+"/prior_page_*.html")    # get the list of raw files

l=len(file_list)

print (parser.prog+": ",l,"new raw files found in the repository." )

if file_list:                    # if the list is not empty, process it 

    for f in file_list:
        timestamp=file_name_timestamp(f)    # extract timestamp from raw file name
        file_name=os.path.basename(f)       # file name without full path
        print (parser.prog+": Processing file: ",file_name)

        with open(f,'r') as in_file:       
            content=in_file.read()          # read content form the raw file 

        df=scrapCurrRatesPrior(content)     # get currency rate information into pandas dataframe

        if df.shape[0]>0:
            loadDF2DB(df,timestamp,args.env)     # load data from dataframe to database
        else:
            print(parser.prog+": No currency rates data found in the file.")

        # compress and save the file to backup floder 

        with gzip.open(os.path.join(rawBackupPath,file_name+'.gz'),'wb') as fl:
            fl.write(content.encode())
        my_repo.git.rm(f)

    # remove processed files from git repository and push this change to GitHub    

    my_repo.git.commit("-m 'Removed loaded raw files'")
    my_repo.remotes.origin.pull()
    my_repo.remotes.origin.push()

