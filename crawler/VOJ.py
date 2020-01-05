import csv
import re
import os
import sys
from io import StringIO
from tqdm import tqdm
from SPOJCrawler import SPOJCrawler

BASE_URL = 'https://vn.spoj.com/'
all_submitted_code = 0
accepted_code_only = 1
def main(crawler, output_dir):
    
    type_get = all_submitted_code
    if sys.argv[-1] == "AC_only":
        type_get = accepted_code_only

    if len(sys.argv) >= 3:
        username = sys.argv[1]
        password = sys.argv[2]
    else:
        username = input('Your username: ')
        password = input('Your password: ')

    crawler._login(username, password)
    output_dir = os.path.join(output_dir, username)

    if type_get == accepted_code_only:
        output_dir = os.path.join(output_dir, 'accepted_code')

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    
    solved_list = crawler.get_solved_list(username)
    submission_count = solved_list.count('\n') 
    print("You have", submission_count, "submissions")
    accepted_submission_count = 0
    
    #|   ID    |        DATE         |  PROBLEM  |  RESULT   | TIME  |  MEM   | LNG |
    csv_reader = csv.reader(StringIO(solved_list), delimiter = '|')
    tBar = tqdm(range(submission_count))
    for i in tBar:
        row = next(csv_reader)[1 : -1]
        if (row == None):
            continue
        row = list(map(str.strip, row))
        
        result = row[3]
        is_AC = (re.match('(AC|100)', result) != None)
        if is_AC:
            accepted_submission_count += 1
            
        if (type_get == accepted_code_only):
            if not is_AC:
                continue
            file_name = row[2]
        else:
            #full information
            file_name = "{2}[{0}][RESULT_{3}][TIME_{4}][MEM_{5}][{1}]".format(row[0], row[1].replace(' ', '_').replace(':','-'), row[2], row[3], row[4], row[5], row[5])
            
            
        crawler.download_solution(os.path.join(output_dir, file_name), username, row[0], row[6])
        tBar.set_description("Accepted submissions found: " + str(accepted_submission_count))
    print("You have", accepted_submission_count, "accepted submissions")
if __name__ == '__main__':
    crawler = SPOJCrawler(BASE_URL,
                BASE_URL + 'files/src/save/{id}')
    output_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    main(crawler, output_dir = output_dir)
