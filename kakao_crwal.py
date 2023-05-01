import os
import re
import pickle
import time
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# 구글 시트 API 사용을 위한 권한 설정
SERVICE_ACCOUNT_FILE = './creds.json'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
creds = None
creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

# 구글 스프레드시트 ID
SPREADSHEET_ID = ''

#시트 이름
sheet_name='테스트중'

# 구글 시트 API 사용 객체 생성
service = build('sheets', 'v4', credentials=creds)

# 메시지 데이터 추출하는 함수
def extract_message_data(text):
    name_pattern = r"1)이름\s*:\s*([^\n]*)"
    birth_year_pattern = r"2)출생년도\s*:\s*([^\n]*)"
    location_pattern = r"3)거주지\s*:\s*([^\n]*)"
    running_time_pattern = r"4)러닝 시간대\s*:\s*([^\n]*)"
    running_pace_pattern = r"5)평균 페이스\s*:\s*([^\n]*)"
    search_route_pattern = r"6)입장 경로\s*:\s*([^\n]*)"
    self_introduction_pattern = r"7)자기표현\s*:\s*([^\n]*)"

    name = re.search(name_pattern, text).group(1).strip()
    birth_year = re.search(birth_year_pattern, text).group(1).strip()
    location = re.search(location_pattern, text).group(1).strip()
    running_time = re.search(running_time_pattern, text).group(1).strip()
    running_pace = re.search(running_pace_pattern, text).group(1).strip()
    search_route = re.search(search_route_pattern, text).group(1).strip()
    self_introduction = re.search(self_introduction_pattern, text).group(1).strip()

    return [name, birth_year, location, running_time, running_pace, search_route, self_introduction]

# 메시지에서 데이터 추출 및 시트에 추가하는 함수


def add_message_data_to_sheet_continuously(name, birth_year, address, running_time, running_pace, entry_path, self_introduction):
    service = build('sheets', 'v4', credentials=creds)
    try:
        # 시트에 데이터 추가
        sheet_values = [[name, birth_year, address, running_time, running_pace, entry_path, self_introduction]]
        request_body = {
            'values': sheet_values
        }
        sheet_name = "테스트중" # 시트 이름
        value_input_option = 'USER_ENTERED'
        insert_data_option = 'INSERT_ROWS'
        service.spreadsheets().values().append(
            spreadsheetId=SPREADSHEET_ID,
            range=f"{sheet_name}!A:A",
            valueInputOption=value_input_option,
            insertDataOption=insert_data_option,
            body=request_body
        ).execute()

    except HttpError as error:
        print(f"An error occurred: {error}")
        sheet_values = []
    except Exception as e:
        print(f"An error occurred: {e}")
        sheet_values = []

    # 시트 데이터 가져오기
    result = service.spreadsheets().values().get(
        spreadsheetId=SPREADSHEET_ID, range=sheet_name).execute()
    values = result.get('values', [])

    # 마지막 행 찾기
    last_row = len(values) + 1

    # 새 데이터 추가할 범위 설정
    new_range = f'{sheet_name}!A{last_row}:G{last_row}'

    # 새 데이터 설정
    new_values = [[name, birth_year, address, running_time, running_pace, entry_path, self_introduction]]

    # 시트에 새 데이터 추가
    request = service.spreadsheets().values().update(
        spreadsheetId=SPREADSHEET_ID, range=new_range,
        valueInputOption='RAW', body={'values': new_values}).execute()
    
    print(f'{request.get("updatedCells")} cells updated.')

with open("./Talk_2023.5.1 12_15-1.txt", "r", encoding='utf-8') as f:
    name, age, address, running_exp, running_time, entry_path, self_intro = None, None, None, None, None, None, None
    for line in f:
        line = line.strip()
        if line.startswith("1)이름"):
            name = line.split(":")[1].strip()
        elif line.startswith("2)나이"):
            age = line.split(":")[1].strip()
        elif line.startswith("3)사는곳"):
            address = line.split(":")[1].strip()
        elif line.startswith("4)러닝경험"):
            if ":" not in line:
                running_exp = None
            else:
                running_exp = line.split(":")[1].strip()
        elif line.startswith("5)러닝 가능시간대"):
            running_time = line.split(":")[1].strip()
        elif line.startswith("6)입장 경로"):
            entry_path = line.split(":")[1].strip()
        elif line.startswith("7)자기표현"):
            self_intro = line.split(":")[1].strip() if len(line.split(":")) > 1 else None
        
        if name and age and address and running_exp and running_time and entry_path:
            print(name, age, address, running_exp, running_time, entry_path, self_intro)
            add_message_data_to_sheet_continuously(name, age, address, running_exp, running_time, entry_path, self_intro)
            name, age, address, running_exp, running_time, entry_path, self_intro = None, None, None, None, None, None, None
