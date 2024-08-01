import gspread
import json
from google.oauth2.service_account import Credentials
from src.get_thresholds import get_thresholds

from sys import argv #argv = [main.py, code, combo, max_raw_mark, max_weighted mark, year]

#thresholds = get_thresholds(argv)

subject_name = argv[1]
max_weighted_mark = int(argv[2])


SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
CREDS = Credentials.from_service_account_file("credentials.json", scopes=SCOPES)
client = gspread.authorize(CREDS)

o_level_sheet_id = "1VHRi9EGKKMJ8FFl9-TWBUoLTrHxa2OfNBzcrZaGM1Dc"
as_level_sheet_id = "1BKJNVW12kINowci9WcdFbwr7JgV7-hKaC_3n7yv7Lh4"
sheets = client.open_by_key(o_level_sheet_id)
if subject_name in map(lambda x:x.title, sheets.worksheets()): 
    worksheet = sheets.worksheet(subject_name)
else: 
    print("Error. Sheet could not be found.")

thresholds : list[list[str]] = worksheet.get_all_values()
new_thresholds : list[list[str]] = thresholds[0:1] #copy table headings

for threshold in thresholds[1:]:
    weight = max_weighted_mark/int(threshold[2])
    new_threshold : list[str] = threshold[0:2] #copy si no and session 
    for mark in threshold[2:]:
        new_threshold.append(str(round(int(mark)*weight)))
    new_thresholds.append(new_threshold)
    
worksheet.update(new_thresholds, 'A1:M20')