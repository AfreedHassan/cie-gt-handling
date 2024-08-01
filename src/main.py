import gspread
import json
from google.oauth2.service_account import Credentials
from src.get_thresholds import get_thresholds
from sys import argv #argv = [main.py, code, combo, max_weighted mark, latest_year, number_of_years]


#paste in your google sheets' sheet ID below
sheet_id = ""

thresholds = get_thresholds(argv)

code = argv[1]

with open("subjectInfo.json", 'r') as f:
    sub_info = json.load(f)
subject_name = sub_info[code]["name"]

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
CREDS = Credentials.from_service_account_file("credentials.json", scopes=SCOPES)
client = gspread.authorize(CREDS) 

sheets = client.open_by_key(sheet_id) #open sheet

#check if sheet already exists, if it does use it, or else add a new sheet with the name of the subject.
if subject_name in map(lambda x:x.title, sheets.worksheets()): 
    worksheet = sheets.worksheet(subject_name)
else: 
    worksheet = sheets.add_worksheet(title=f"{subject_name}", rows=100, cols=26)

#update the cells of the worksheet
worksheet.update(thresholds, 'A1:M20')
