# vagd illo mendra e sigt
import io
import os
import json
import time

from   PIL       import Image
from   copy      import deepcopy
from   pdf2image import convert_from_path as CFP

from base64 import (
    b64encode as b64e,
    b64decode as b64d
)


# region functions
applyGuideSet = lambda pos, guitdeSet: tuple(map(sum, zip(pos, guitdeSet)))

isSameType = lambda t: all(isinstance(x, type(t[0]))for x in t)

def cropImage(outputFolder, page, nameList, name:int|str, cropArea):
    if not os.path.exists(outputFolder):
        os.makedirs(outputFolder)
        print("폴더가 새로 생성되었습니다.")

    page.crop(cropArea).save(
        os.path.join(
            outputFolder,
            (
                f"{nameList[name]}.png"\
                    if isinstance(name, int)\
                else f"{name}.png"
            )
        ),
        'PNG'
    )

def PdftoImages(outputFolder, pages, nameList, cropData:list):
    if not os.path.exists(outputFolder):
        os.makedirs(outputFolder)
        print("폴더가 새로 생성되었습니다.")

    for i, image in enumerate(pages):
        a = cropArea['type'][cropData[0][i]]
        cropImage(
            outputFolder,
            image, nameList, i,
            applyGuideSet(
                a if type(cropData[0][i])==str else cropData[0][i],
                list(cropArea['guideSet'].values())[cropData[1]]['set']
            )
        )
        print(f"'{nameList[i]}'의 이미지가 크롭 후 저장되었습니다.")

def savePDFData(dataPath, pages, saveType:str="make", target:dict={}) -> None:
    """
    saveType : str = make || append
    """
    with open(dataPath, "w") as f:
        for i, obj in enumerate(pages):
            a = time.time()
            print(f"{i+1}번째 페이지 데이터 추출 중...", end=' ')
            buffer = io.BytesIO()
            obj.save(buffer, 'PNG')
            pages[i] = buffer.getvalue()
            print(f"완료! : {time.time() - a:.2f}초 소요됨")

        if saveType == "make":
            json.dump({path : b64e(str(pages).encode()).decode()}, f)

        elif saveType == "append":
            target[path] = b64e(str(pages).encode()).decode()
            json.dump(target, f)


# region data
names = {
    "EXT:IV" : [
        "DIE IN",
        "LUV",
        "ADDICT!ON",
        "Like a Fool",
        "너에게로 갈래",
        "Hypernaid",
        "The Four Seasons Summer 2017",
        "Love.Game.Money",
        "Stay Alive",
        "Deadly Bomber",
        "Weaponize",
        "New World",
        "Hyper Drive",
        "Stolen Memory",
        "Hell'o",
        "Vertical Eclipse",
        "Back to the oldschool",
        "!!New Game Start!!",
        "Gloxinia",
        "Don't Cry",
        "LUV (Extended Ver.)",
        "Like A Fool (Extended Ver.)",
        "The Four Seasons Summer 2017 (Extended Ver.)",
    ],

    "EXT:V" : [
        "glory MAX -너의 최대치로 너와 함께할게-",
        "My Wonderland",
        "별빛너머",
        "Inside the Light",
        "ECiLA",
        "Shining Light",
        "Right Time",
        "Paradise",
        "S.A.V.E",
        "Pitter-patter",
        "Accelerate",
        "Carrot Carrot",
        "Rhapsody for the VEndetta",
        "God Machine",
        "Behemoth",
        "Rocket Launcher",
        "Revenger",
        "Critical Point",
        "3_33",
        "Peace Comes At a Price",
        "별빛너머 (Extended Ver.)",
        "Shining Light (Extended Ver.)",
        "Accelerate (Extended Ver.)",
        "Peace Comes At a Price (Extended Ver.)",
    ] 
}

cropArea = {
    "type" : {
        "right"  : (2588, 1095, 4962, 3469),
        "middle" : (1665, 1095, 4039, 3469),
        "left"   : (742, 1095, 3116, 3469),
    },
    "guideSet" : {
        "EXT:IV" : {
            "name" : "\033[31mEXT:IV\033[0m",
            "set"  : (0, 0, 0, 0)
        },

        "EXT:V" : {
            "name" : "\033[33mEXT\033[34m:V\033[0m",
            "set"  : (-353, -131, -369, -146)
        }
    }
}
# 2374x2374

PDFDataPreset = None
dataPath = f"{os.getcwd()}/pdfData.json"

hi = '\n    '


# region system
print("세이브 데이터 불러오는 중...", end=' ')
try:
    with open(dataPath, "r") as f:
        PDFDataPreset = json.load(f)
    print("완료!")
except:
    pass
    print("실패! : 세이브 데이터가 존재하지 않습니다.")
print("\n")

while 1:
    if (outputFolder := input("\033[33m저장할 폴더의 이름\033[0m을 정해주세요 : \033[33m")):
        break
    print("\033[0m", end='')
    continue

print(f"\033[0m폴더 이름 : \033[33m{outputFolder}\033[0m\n\n")

input("좋습니다. 이제 \033[31mPDF 파일\033[0m을 특정할 차례입니다.\n\n확인__")
print("\n")
while 1:
    try:
        path = input("추출할 \033[31mPDF 파일\033[0m의 \033[35m위치\033[0m를 정해주세요\033[32m(끝에 .pdf 확장자를 포함해야 합니다. 이 파일이 실행된 폴더 내를 기준으로 상대경로를 입력해주세요)\033[0m : ")

        if PDFDataPreset and path in PDFDataPreset:
            if input("이미 추출된 데이터가 존재합니다. 추출된 데이터를 사용할까요?(확인 : y, 취소 : Any\033[31m(not y||Y)\033[34m(기본값)\033[0m) : ").lower() == 'y':
                pages = eval(b64d(PDFDataPreset[path]).decode())

                for i, obj in enumerate(pages):
                    a = time.time()
                    print(f"{i+1}번째 페이지 데이터 로드 중...", end=' ')
                    pages[i] = Image.open(io.BytesIO(obj))
                    print(f"완료! : {time.time() - a:.2f}초 소요됨")

                break
            
        print("데이터 추출 중...")
        pages = CFP(path, dpi=1000, poppler_path='poppler-24.08.0/Library/bin')[2:]
        print("추출이 완료되었습니다.\n\n")

        print("세이브 데이터 검사 중...")
        if not os.path.exists(dataPath):
            if input("세이브 데이터가 없습니다. 새로 생성할까요?(확인 : y, 취소 : Any\033[31m(not y||Y)\033[34m(기본값)\033[0m) : ").lower() == 'y':
                savePDFData(dataPath, deepcopy(pages))
        else:
            if input("추출된 \033[31mPDF 데이터\033[0m를 저장할까요?(확인 : y, 취소 : Any\033[31m(not y||Y)\033[34m(기본값)\033[0m) : ").lower() == 'y':
                with open(dataPath, "r") as f:
                    PDFDataPreset = json.load(f)
                
                savePDFData(dataPath, deepcopy(pages),
                            saveType="append",
                            target=PDFDataPreset
                                                )
        break

    except Exception as e:
        print(f"Error occured! : \033[31m{e}\033[0m\n뭐 그렇다네요 돌아가세요\n\n")
        continue

input(f"\n감지된 페이지 수 : {len(pages)}\n\033[32m(해당 페이지 수는 가장 앞에 있는 커버와 리스트를 제거한 수입니다.)\033[0m\n\n확인__")

width, height = pages[0].size
input(f"\n\n전체 이미지 사이즈 : \033[34m{width}x{height}\033[0m\n\n확인__")

while True:
    try:
        # choice = int(input(f"\n\n크롭 프리셋을 선택해주세요 :\n    {hi.join(map(lambda l: f'{l[0]} : {l[1]}', chain(enumerate(cropArea['guideSet'].keys()))))}\n\n>>> "))
        choice = {}
        choice['num'] = int(input(f"\n\n크롭 프리셋을 선택해주세요 :\n    {hi.join(map(lambda l: f'{l[0]} : {l[1]}', enumerate(map(lambda gs: gs['name'], cropArea['guideSet'].values()))))}\n\n>>> "))
        choice['name'] = list(cropArea['guideSet'].keys())[choice['num']]

        for i, typ in enumerate(("left", "middle", "right")):
            cropImage(
                outputFolder,
                pages[0], None, f"샘플_{typ}",
                applyGuideSet(cropArea['type'][typ], list(cropArea['guideSet'].values())[choice['num']]['set'])
            )
        input(f"\n\n샘플 커버 이미지 세 개가 크롭되었습니다. \033[33m'{outputFolder}'\033[0m 폴더에서 확인해주세요\n\n확인__")
        if input("\n\n이상이 없다면 done을 입력해주세요\n\n>>> \033[33m").lower() == 'done':
            break

    except Exception as e:
        print(f"Error occured! : \033[31m{e}\033[0m\n뭐 그렇다네요 돌아가세요\n\n")
        continue

input(f"\033[0m\n\n다음으로 \033[35m크롭 위치\033[0m를 설정해야 합니다.\n\n확인__")

cropTypeMenu   = ('1. 왼쪽', '2. 중간', '3. 오른쪽', '', '또는... 직접 입력\033[32m(\'x\')\033[34m(이 예시는 현재 위치(middle 기준)에서 이동할 정도를 나타냅니다.)\033[0m')
cropTypeOption = {'1' : "left", '2' : "middle", '3' : "right"}
cropData       = []

for name in names[choice['name']]:
    while 1:
        try:
            match (cropC := input(f"\n\n\033[32m'{name}'\033[0m에 알맞은 크롭 위치를 정해주세요:\n    {hi.join(cropTypeMenu)}\n\n>>> \033[33m")):
                case '1'|'2'|'3': cropData.append(cropTypeOption[cropC])
                case _:
                    if isinstance(int, (cropC:=eval(cropC))):
                        cropData.append((cropC, 0, cropC, 0))
 
            break

        except Exception as e:
            print(f"\033[0mError occured! : \033[31m{e}\033[0m\n뭐 그렇다네요 돌아가세요\n\n")
            continue
print("\033[0m", end='')

PdftoImages(
    outputFolder,
    pages,
    names[choice['name']],
    [cropData, choice['num']]
)