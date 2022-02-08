This is a simple python program that analyses a log file downloaded from the url provided or from a backup archive. 
The program groups log entries for each day present in the log and counts the top N clients or requests for that day.

To provide a url to download an archive of a log file use the optional <code>-url</code> argument

To change the number of results per day use the optional <code>-n</code> argument

To select clients or requests use the <code>-get_frequent</code> argument



Examples:

<code>
python3 main.py -get_frequent clients
</code>

  - will use the backup archive as url was not provided
  - will use the default number of top clients per day which is 2
  
<code>
python3 main.py -get_frequent requests -url 'https://example.com/archive.gz' -n 5
</code>

  - will try to download the archive at the url provided, save it in the data folder and extract the log file there 
  - will use the provided number of top requests per day which is 5

The requirements.txt file includes the python version as well as the pip packages that I have used to run the program. I suspect that older or newer versions would work just as well but I did not dedicate time to check this so in case of issues update to the versions mentioned in requirements.txt.

The programs prints out in the command line the results for simplicity of use but this can easily be changed to output to file for example.

Plans for future improvements:
  - design unit testing for the program
  - analyse data that is not loaded (in the step that loads into dataframe on_bad_lines='skip' is used) and see if more data can be used
  - generate some plots based on the results
  - check other metrics that could show insights into the data (e.g. look at responses maybe corelation between 4xx response vs requests etc)
