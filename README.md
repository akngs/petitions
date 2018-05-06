[청와대 국민청원](https://www1.president.go.kr/petitions) 사이트의
[만료된 청원](https://www1.president.go.kr/petitions?only=finished) 데이터 모음.

## 데이터

[petition.csv](https://s3.ap-northeast-2.amazonaws.com/data10902/petition/petition.csv)

* 전체 데이터

[petition_corrupted.csv](https://s3.ap-northeast-2.amazonaws.com/data10902/petition/petition_corrupted.csv)

* 전체 행 중에서 5%는 임의 필드 1개에 결측치 삽입
* 범주(category)가 '육아/교육'이고 투표수(votes)가 50건 초과이면 20% 확률로 투표수에 결측치 넣기
* 나머지는 전체 데이터와 동일

[petition_sampled.csv](https://s3.ap-northeast-2.amazonaws.com/data10902/petition/petition_sampled.csv)

* 전체 데이터 중 5%만 임의추출한 데이터

## 저작권

CSV 데이터의 저작권은 [KOGL 제1유형](http://www.kogl.or.kr/info/license.do)을 따름.

* 출처표시
* 상업적, 비상업적 이용가능
* 변형 등 2차적 저작물 작성 가능

소스 코드는 [MIT License](LICENSE)를 따름.

## 설치 및 실행

소스코드 받기:

    git clone https://github.com/akngs/petitions.git
    cd petitions

설치 ([pipenv](https://github.com/pypa/pipenv)가 설치되어 있어야 합니다):

    pipenv install

실행:

    pipenv shell
    python petition.py

생성된 데이터 확인:

    tail data/*.csv
