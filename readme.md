This is a simple python program that analyses a log file downloaded or from a backup archive. The program groups log entries for each day present in the log and counts the top N clients or requests for that day.

To provide a url to download an archive of a log file use the optional -url argument
To change the number of results per day use the optional -n argument
To select clients use the -get_frequent argument

Examples:
'''
python3 main.py -get_frequent clients
'''
will use the backup archive as url was not provided
will use the default number of top clients per day which is 2

'''
python3 main.py -get_frequent requests -url 'https://example.com/archive.gz' -n 5
'''
will try to download the archive eat the url provided, save it in the data folder and extract the log file there 
will use the provided number of top requests per day which is 5
