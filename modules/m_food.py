import sys, random

if __name__=="__main__":
    print("FATAL   : Run this bot from right way.")
    sys.exit(1)

DB_VERSION = "19121401_fix"

lf_list = ["메가맥 세트에서 야채 다 빼고 ㄱ",
           "이마트24 가서 속풀라면 ㄱ",
           "고씨네 가서 소고기카레 1고 ㄱ",
           "단지네 가서 콩나물국밥 ㄱ",
           "맘스터치 치킨 좋음",
           "김치킨 짜긴한데 맛있음",
           "지정환피자 크런치골드 라지 ㄹㅇ 갓피자임",
           "BBQ 황금올리브 ㄹㅇ 갓치킨임 꼭먹으셈",
           "상문이두마리 간장치킨 ㄱ 교촌보다는 **싸서** 맛있음",
           "옛날통닭 맛있음 개추",
           "이마트 치킨 맛있는데 왜 아무도 관심을 안주죠",
           "교촌 간장치킨 비싼데 맛있음 ㅇㅇ",
           "굽네 볼케이노 개맛있음",
           "저 갱상도 새럼이라서 냉면에다 식초랑 겨자 오지게 많이넣음",
           "이마트 피코크 군만두 개맛있는데 왜 아무도 안사죠",
           "짜장면에 고춧가루 오지게 뿌려서 안먹어본 사람은 있어도 한번만 먹어본 사람은 없음",
           "솔직히 오리지널 양념치킨도 맛있지 않음?",
           "가성비의 맛 버거킹 사딸라",
           "마라맛을 싸게 느끼고 싶다면 지금바로 CU로 ㄱㄱ",
           "냉면장인들의 서식지 진주로 오시오",
           "지코바 소금구이는 굽네치킨을 넘어선 갓 치킨입니다",
           "아 소고기먹고싶다",
           "BHC도 후라이드 나쁘지 않음",
           "KFC 닭껍질튀짐은 좀 비추",
           "롯데리아 지파이는 안먹어봐서 모르겠네요 정보가 유익하셨다면 구독과 좋아요를 삐슝뿌슝빠슝",
           "맥도날드 앱 깔고 회원가입하면 빅맥 단품이 1000원?!",
           "맥도날드 아보베 먹어본 후기 : 뭔가 녹즙맛이 남",
           "버블티는 공차가 좋지만 이디야도 좋음",
           "GS25 탄탄멘(일본음식아님) 뭔가 오묘하게 맛있음",
           "고씨네 2고 정도는 거뜬하게 버티는 사람이라면 네넴띤도 도전 ㄱㄱ",
           "세트로 한끼를 든든하게 채울 수 있는 버거킹 몬스터와퍼",
           "제작자의 서브웨이 픽 1 : 터키 (파마산 오레가노, 슈레드, 양상추+양파+올리브만, 사우스 웨스트)",
           "제작자의 서브웨이 픽 2 : BLT (+페퍼로니, 파마산 오레가노 + 슈레드 + 양상추 양파 올리브 + 사우스 웨스트 + 올리브 오일)",
           "제작자의 아침저녁에는 마늘장아찌가 무조건 들어감",
           "이마트 고메 함박스테이크 데워서 밥이랑 섞어먹어보셈",
           "제작자는 스팸을 통으로 구워먹는거라고 배웠습니다",
           "후라이드 잘하는 집 = 말그대로 후라이드 잘함",
           "건조밀웜 저만맛있나요",
           "제작자의 평균적인 스파게티 조리실력이 그대로 느껴지는 GS25 치킨 아라비아따 스파게티",
           "이건 좀 너무하다 싶은 양의 농심 스파게티",
           "이지투하다 체력이 바닥나면 맥도날드 에그불고기 버거",
           "맥도날드 메가맥 ㄱ?",
           "닭가슴살을 잘 살리는 지코바",
           "파인애플을 잘 살리는 지정환피자",
           "주말에는 피시앤칩스",
           "라면에 케첩이나 카레를 넣으면 맛있습니다 구라아님",
           "닭껍질튀김 + 뿌링클가루 = :blush:",
           "왕뚜껑이 작아지면 도시락",
           "이마트 해쉬브라운 20개 한박스가 4,980원?!",
           "베이컨은 온라인에서 1kg당 만원 초반대",
           "시원하진 않지만 아무튼 시원한 동태탕",
           "춥진 않지만 아무튼 추어탕",
           "쫄깃한 내장국밥 ㄱㄱ",
           "배고프면 뭘 먹어도 맛있음 ㅇㅇ",
           "민트초코마이쩡"]

ELEMENT_COUNT = str(len(lf_list))

def return_food():
    return(random.choice(lf_list))
