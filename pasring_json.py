import json
import os
from tqdm import tqdm
from glob import glob

#/label디렉토리에 있는 json 파일 이름을 리스트로 불러옵니다.
json_file = glob("label/*.json")
print(len(json_file))

#클래스 담을 list 선언
food_class = ['baeghyang-gwa', 'beigeulsaendeuwichi', 'bibimbab', 'bogsung-a', 'bokk-eumbab', 'bokk-eummyeon', 'bossam', 'korean_style_pancake', 'ppang', 'sagwapai']
print(len(food_class))
label_list = []

# json 파일 반복 돌면서 데이터 빼내기
for jsons in tqdm(json_file):
    # 오류가 없으면 json 파일을 엽니다.
    with open(f'{jsons}') as file:
        #json 파일 로드
        datas = json.load(file)
        
        tmp_list = []
        # json 데이터에서 class, 너비, 높이, 중심(x,y) 추출
        for i in datas:
            if i['Name'] == 'bibimbap':
                name = 'bibimbab'
            elif i['Name'] == 'peach':
                name = 'bogsung-a'
            else:
                name = i['Name']
            width = i['W']
            height = i['H']
            point = i['Point(x,y)']
            tmp_list.append([food_class.index(name),float(point.split(',')[0]),float(point.split(',')[1]),float(width),float(height)])
            
        #     print(name,width,height,point)
        # print(tmp_list)

        # class를 리스트에 추가
        # if name in food_class:
        #     pass
        # else:
        #     food_class.append(name)


        # (작성 순서: class 번호 x중심좌표 y중심좌표 width heigth)
        #                   class 번호 부여         '0.xx,0.xx' 생긴걸 , 를 기준으로 분리 후 float()으로 실수 변환    실수 변환            img이름 변경을 위한 json 이름 정보 추가  
        label_list.append([tmp_list,jsons])
# print(food_class)
# food_class.sort()
# print(food_class) . . . . . . . .     
# class 번호순으로 오름차순
label_list.sort()
for i in label_list:
    print(i)
# .text 저장할 디렉토리 최초 1회 실행
os.mkdir('labels')
# os.mkdir('image')

# 번호순으로 정렬된 리스트를 반복문 돌면서 text 파일 생성 및 작성
for i, coordinate in enumerate(label_list):
    # 'label/A020511XX_02583.json' 에서 A020511XX_02583 이것만 추출
    label = coordinate[0]
    json_name = coordinate[1]
    old_file_name = json_name[6:-5]

    # A020511XX_02583.jpg 파일을 -> 0_frame_000000.jpg 이런 식으로 변경
    # os.rename(f'images/{old_file_name}.jpg', f'image/{label[0][0]}_frame_{i:06d}.jpg')

    # text 파일을 쓰기 위해 파일 오픈
    yolo_file = open(f'labels/{label[0][0]}_frame_{i:06d}','w')
    for j in label:

        #write()에 파라미터가 1개 밖에 안들어감 그래서 5개 각각 작성
        yolo_file.write(f'{j[0]} ')
        yolo_file.write(f'{j[1]} ')
        yolo_file.write(f'{j[2]} ')
        yolo_file.write(f'{j[3]} ')
        yolo_file.write(f'{j[4]}')


    yolo_file.close()