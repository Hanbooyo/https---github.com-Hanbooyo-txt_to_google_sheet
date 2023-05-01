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
SPREADSHEET_ID = '1yLAnbS1k6oWhktaTDYN8gC-Q2NbLePrZEg0j8JhaBuI'

#시트 이름
sheet_name='테스트중'

# 구글 시트 API 사용 객체 생성
service = build('sheets', 'v4', credentials=creds)

# 메시지에서 데이터 추출 및 시트에 추가하는 함수
def add_message_data_to_sheet_continuously(data):
    service = build('sheets', 'v4', credentials=creds)
    try:
        # 메시지에서 데이터 추출
        name = data['name'] 
        birth_year = data['age']
        address = data['address']
        running_time = data['running_time']
        running_pace = data['running_exp']
        entry_path = data['entry_path']

        # 시트에 데이터 추가
        sheet_values = [[name, birth_year, address, running_time, running_pace, entry_path]]
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

        # 시트 데이터 가져오기
        result = service.spreadsheets().values().get(
            spreadsheetId=SPREADSHEET_ID, range=sheet_name).execute()
        values = result.get('values', [])

        # 마지막 행 찾기
        last_row = len(values) + 1

        # 새 데이터 추가할 범위 설정
        new_range = f'{sheet_name}!A{last_row}:G{last_row}'

        # 새 데이터 설정
        new_values = [[name, birth_year, address, running_time, running_pace, entry_path]]

        # 시트에 새 데이터 추가
        request = service.spreadsheets().values().update(
            spreadsheetId=SPREADSHEET_ID, range=new_range,
            valueInputOption='RAW', body={'values': new_values}).execute()

        print(f'{request.get("updatedCells")} cells updated.')

    except HttpError as error:
        print(f"An error occurred: {error}")
    except Exception as e:
        print(f"An error occurred: {e}")

with open('./Talk_2023.5.1 12_15-1.txt', 'r', encoding="utf-8") as f:
    data = {}
    for line in f:
        line = line.strip()
        print(line)
        if "1)이름" in line: #startswith가 아니었음
            try:
                data['name'] = line.split(":")[3].strip()
                line = f.readline().strip()
                if data['name'] != "":
                    print("name",data['name'])
                    time.sleep(3)
            except IndexError:
                continue
            if data['name'] and data['name'] != '방장봇':
                if line.startswith('2)'):
                    data['age'] = line.split(':')[1].strip()
                    print(data['age'])
                    line = f.readline().strip()
                    if line.startswith('3)'):
                        data['address'] = line.split(':')[1].strip()
                        print(data['address'])
                        line = f.readline().strip()
                        if line.startswith('4)'):
                            data['running_exp'] = line.split(':')[1]
                            print(data['running_exp'])
                            line = f.readline().strip()
                            if line.startswith('5)'):
                                data['running_time'] = line.split(':')[1].strip()
                                print(data['running_time'])
                                line = f.readline().strip()
                                if line.startswith('6)'):
                                    data['entry_path'] = line.split(':')[1].strip()
                                    print(data['entry_path'])
                                    line = f.readline().strip()
                                    if line.startswith('20'):
                                        add_message_data_to_sheet_continuously(data)
                                        data = {}
                                        time.sleep(3)
                                        continue      
