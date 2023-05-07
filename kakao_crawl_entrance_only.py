import time
from google.oauth2 import service_account
from googleapiclient.discovery import build

# 구글 시트 API 사용을 위한 권한 설정
SERVICE_ACCOUNT_FILE = './creds.json'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
creds = None
creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

# 구글 스프레드시트 ID
SPREADSHEET_ID = '1yLAnbS1k6oWhktaTDYN8gC-Q2NbLePrZEg0j8JhaBuI'

# 구글 시트 API 사용 객체 생성
service = build('sheets', 'v4', credentials=creds)

# 메시지에서 데이터 추출하는 함수
def extract_data_from_message(data):
    date_time = data.get('date_time')
    name = data.get('name')  
    return [date_time, name]     
        

# 메시지에서 데이터 추출하는 함수
def extract_enter_message(data):
    date_time = data.get('date_time')
    name = data.get('name')
    return [date_time, name]

# 시트에 데이터 추가하는 함수
def append_data_to_sheet(values):
    service = build('sheets', 'v4', credentials=creds)
    sheet_name = '입장일'  # 시트 이름
    range_name = f'{sheet_name}!A:G'
    value_input_option = 'USER_ENTERED'

    # 시트 데이터 가져오기
    result = service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID, range=range_name).execute()
    values = result.get('values', [])

    # 마지막 행 찾기
    last_row = len(values) + 1

    # 새 데이터 추가할 범위 설정
    new_range = f'{sheet_name}!A{last_row}:G{last_row}'

    # 새 데이터 설정
    new_values = [extract_data_from_message(data)]

    # 시트에 새 데이터 추가
    request = service.spreadsheets().values().update(
        spreadsheetId=SPREADSHEET_ID, range=new_range,
        valueInputOption=value_input_option, body={'values': new_values}).execute()

    print(f'{request.get("updatedCells")} cells updated.')

# 메시지에서 추출한 데이터를 시트에 추가
def add_message_data_to_sheet(data):
    values = extract_data_from_message(data)
    append_data_to_sheet(values)

with open('./Talk_2023.5.1 12_15-5.txt', 'r', encoding="utf-8") as f:
    data = {}
    for line in f:
        line = line.strip()
        if "님이 들어왔습니다." in line:
            print(line)
            data = {}
            parts = line.strip().split(':')
            data['date_time'] = parts[0]+":"+parts[1] 
            data['name'] = parts[2].replace("님이 들어왔습니다.","")
            add_message_data_to_sheet(data)
  
