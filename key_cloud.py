import matplotlib.font_manager as fm 
from wordcloud import WordCloud
from PIL import Image
import numpy as np



# 이용 가능한 폰트 중 '고딕'만 선별
for font in fm.fontManager.ttflist:
    if 'Gothic' in font.name:
        print(font.name, font.fname)

font_path = 'C:/Windows/Fonts/malgunbd.ttf'

text = ""
 
with open("KakaoTalk_20230507_1511_32_574_group.txt", 'r', encoding = "utf-8") as txt :
    lines = txt.readlines()
    for line in lines[4:] :
        if '] [' in line :
            text += ( line.split('] ')[2].replace('이모티콘\n', "")
            .replace("사진\n", "").replace('삭제된 메세지입니다.\n', "").replace("샵검색", '').replace('채팅방 관리자가 메시지를 가렸습니다.','').replace('동영상','').replace('사진','').replace('2장','') 
             .replace('공지방 입장코드는','').replace('자기소개','').replace('https','').replace('삭제된 메시지입니다','')
             .replace('오늘','').replace('저는','').replace('저도','').replace('비번 입니다.','').replace('비번 입니다','')
             .replace('ㅋ','').replace('ㅎ','').replace('안녕하세요','').replace('네','').replace('지봉',''))
        
print(text)


mask = np.array(Image.open('love2.png'))
wc = WordCloud(font_path='C:/Windows/Fonts/malgunbd.ttf', background_color="white", mask=mask, width = 1200, height = 1200)
wc.generate(text)
wc.to_file("result_masked3.png")