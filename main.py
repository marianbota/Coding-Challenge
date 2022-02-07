import os
import requests
import gzip
import shutil
import argparse 

import pandas as pd


argparser = argparse.ArgumentParser(description='Coding challenge')
argparser.add_argument('-get_frequent', type=str, help='Choose to get most frequent clients or requests per day', choices=[
                       'clients', 'requests'])
argparser.add_argument('-url', type=str, help='Please provide the url for the gzip archive')
argparser.add_argument(
    '-n', type=int, help='Please provide the number of top results per day')
args = argparser.parse_args()

class Challenge:
    def __init__(self):
        '''
        It seams that making the request without headers results in a 406 error. 
        I am assuming that this is part of the challenge and I am not breaking anyone's wishes to not be scraped by impersonating a Mozilla user-agent
        '''
        self.headers = {
            "User-Agent":
            "Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0"
        }
        self.url = None
        self.dest_folder = None
        self.archive_path = None
        self.file_name = None
        self.n = None
    
    
    def download(self):

        # create folder if it does not exist
        if not os.path.exists(self.dest_folder):
            os.makedirs(self.dest_folder)  

        # replace spaces with underscores
        self.archive_name = self.url.split('/')[-1].replace(" ", "_")
        self.archive_path = os.path.join(self.dest_folder, self.archive_name)
        

        r = requests.get(self.url, headers=self.headers, stream=True, allow_redirects=True)
        if r.ok:
            print("SUCCESS: Saving to", os.path.abspath(self.archive_path))
            with open(self.archive_path, 'wb') as f:
                f.write(r.content)
        else:  # HTTP status code 4XX/5XX
            print("Download failed: status code {}\n{}".format(r.status_code, r.text))


    def extract(self):
        print("Extracting file from", os.path.abspath(self.archive_path))

        # get name of file from archive
        self.file_name = os.path.splitext(self.archive_path)[0]

        #extract the file in the same folder as archive
        with gzip.open(self.archive_path, 'rb') as f_in:
            with open(self.file_name, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)

    def get_frequent_clients(self):

        # read the log file into pandas dataframe
        df = pd.read_csv(self.file_name, sep='\s+', lineterminator='\n',
                         encoding='ISO-8859-1', on_bad_lines='skip', header=None)
        
        # add column date as the day extracted from the timestamp
        df['date'] = pd.to_datetime(
            (df[3]+df[4]), format="[%d/%b/%Y:%H:%M:%S%z]").dt.to_period('D')

        # rename columns to better understand what they represent
        df.rename(columns={0: 'client', 5: 'request',
                  6: 'response', 7: 'size'}, inplace=True)

        # group by date and client and calculate count of occurences per each group
        group_by_date_client = df.groupby(['date', 'client']).size().to_frame('count')

        # sort the data based on count in descending order
        sorted = group_by_date_client.groupby(['date']).apply(
            lambda x: x.sort_values(['count'], ascending=False))
        
        # filter only the first n results per date
        result = sorted.groupby(['date']).head(self.n)
        return(result)

    def get_frequent_requests(self):
        # read the log file into pandas dataframe
        df = pd.read_csv(self.file_name, sep='\s+', lineterminator='\n',
                         encoding='ISO-8859-1', on_bad_lines='skip', header=None)

        # add column date as the day extracted from the timestamp
        df['date'] = pd.to_datetime(
            (df[3]+df[4]), format="[%d/%b/%Y:%H:%M:%S%z]").dt.to_period('D')

        # rename columns to better understand what they represent
        df.rename(columns={0: 'client', 5: 'request',
                  6: 'response', 7: 'size'}, inplace=True)

        # group by date and request and calculate count of occurences per each group
        group_by_date_client = df.groupby(
            ['date', 'request']).size().to_frame('count')
        
        # sort the data based on count in descending order
        sorted = group_by_date_client.groupby(['date']).apply(
            lambda x: x.sort_values(['count'], ascending=False))

        # filter only the first n results per date
        result = sorted.groupby(['date']).head(self.n)
        return(result)



if __name__ == '__main__':
   

    challenge = Challenge()
    if not args.n:
        print('Number of top results not set, using default value of 2')
        challenge.n = 2
    else:
        challenge.n = args.n

    if not args.url:
        print('URL not provided, using backup data from the backup folder')
        challenge.dest_folder = 'backup'
        challenge.archive_path = os.path.join(
            challenge.dest_folder, 'backup_NASA_access_log_Jul95.gz')
        challenge.file_name = os.path.splitext(
            challenge.archive_path)[0]
    else:
        challenge.url = args.url
        challenge.dest_folder = 'data'
        challenge.download()
        challenge.extract()
    if args.get_frequent == 'clients':
        result = challenge.get_frequent_clients()
    elif args.get_frequent == 'requests':
        result = challenge.get_frequent_requests()
    print(result)
