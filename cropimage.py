import json
import os 
import os.path
import glob
from PIL import Image


# data_sample 주소 입력
path = 'C:/Users/user/Desktop/wkit/data_sample' 

file_list1 = os.listdir(path)

i = 0

# file_list1 -> ['falldown_79_6255', 'falldown_324_8154', 'falldown_407_6980']
# file_list2[0] -> ['rgb']
# len(file_list1) -> 3


#폴더가 몇개 있든 유동적으로 실행될 수 있게
while i < ((len(file_list1))):

  second_path = f"{path}/{file_list1[i]}"
  #디렉토리가 아닌 파일이 있을시 (.py .DS_Store 등) 아래코드를 실행하지 않고 반복문으로 넘어감
  if os.path.isdir(f'{path}/{file_list1[i]}') == False:
    i += 1 
    continue

  file_list2 = os.listdir(second_path)

  rgb_path = f"{path}/{file_list1[i]}/{file_list2[0]}"
  # print(rgb_path)

  
  json_path = glob.glob(f"{rgb_path}/*.json", recursive=True)
  # print(json_path)

  # result 폴더 만들기
  result_folder = f'{second_path}/result'

  if not os.path.isdir(result_folder):
    os.mkdir(result_folder)


  # JSON 파일, PNG파일

  num = 1 # 파일이름위한변수

  while num <= (len(json_path)):

      with open(f"{rgb_path}/{num}.json" , "r", encoding="utf8") as f:
          contents = f.read()
          json_data = json.loads(contents) # JSON 파일


      image = Image.open(f"{rgb_path}/{num}.png") # PNG파일


      x = 0 # label 이름 출력 위한 변수



      while x < (len(json_data["shapes"])):


          labelname = json_data["shapes"][x]["label"] # Label 이름
          
          print(num,".json파일의", x+1, "번째 레이블 출력 :", labelname)

          point1 = json_data["shapes"][x]["points"][0][0]
          point2 = json_data["shapes"][x]["points"][0][1]
          point3 = json_data["shapes"][x]["points"][1][0]
          point4 = json_data["shapes"][x]["points"][1][1]

          # point1,2,3,4,를 순서대로 왼쪽 위 오른쪽 아래 라고 하였을때
          # point1과 point3 즉 왼쪽과 오른쪽의 값을 비교하여 더 큰쪽이 오른쪽 값이 될 수 있도록
          # point2, point4 위 값과 아랫 값을 비교하여 큰값이 윗값이 되도록 설정하여 오류가 없게함.
          if(point1 > point3):
            point1 = json_data["shapes"][x]["points"][1][0]
            point3 = json_data["shapes"][x]["points"][0][0]

          if(point2 > point4):
            point2 = json_data["shapes"][x]["points"][1][1]
            point4 = json_data["shapes"][x]["points"][0][1]

          croppedImage=image.crop((
              point1, point2, point3, point4
          ))

          #라벨이름을 동적으로 none, assault, swoon 이외의 라벨이있어도 실행 될수 있도록
          label_folder = f'{result_folder}/{labelname}' # label이름으로 디렉토리 생성


          #디렉토리가 없는경우 생성하여 오류가 없도록
          if not os.path.isdir(label_folder):
            os.mkdir(label_folder)
            
            
          #none파일 이름의 중복으로 파일 저장 안되는 문제 {x+1}로 저장
          croppedImage.save(f'{label_folder}/{num}_{labelname}{x+1}.PNG')

          
          x += 1
      num += 1

  i += 1


