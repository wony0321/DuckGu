# 김도영 공식 팬클럽의 최종 프로젝트
### - 영화 추천 알고리즘 기반 커뮤니티 서비스

<br/>

# 1. 요구사항
## 개요

- 영화 데이터 기반 추천 웹 서비스 개발
- 영화 추천 알고리즘 구현
- 커뮤니티 서비스 구성
- 서비스 관리 및 유지보수
  
## 필수 요구사항

1) 영화 데이터

  - 영화 정보 데이터는 최소 50개 이상 존재해야 함
  - fixtures를 사용하여 언제든 load 될 수 있는 초기 데이터가 있어야 함

2) 영화 추천 알고리즘

  - 사용자는 반드시 최소 1개 이상의 영화를 추천받을 수 있어야 함
  - 추천 방식은 자유롭게 구성 가능
  - 어떠한 방식으로 추천 시스템을 구현했는지 기술적으로 설명할 수 있어야 함

3) API

 - API 사용 제한 없음(TMDB, Youtube API 등)

4) 커뮤니티

 - 유저 간 소통할 수 있는 커뮤니티 기능 구현
 - 커뮤니티 기능은 반드시 게시판 형식일 필요는 없으며, 소통이라는 관점 안에서 다양한 방법으로 자유롭게 구현 가능

5) README

   - 팀원 정보 및 업무 분담 내역
    - 목표 서비스 구현 및 실제 구현 정도
    - 데이터 베이스 모델링(ERD)
    - 영화 추천 알고리즘에 대한 기술적 설명
    - 핵심 기능에 대한 설명
    - 기타(느낀점, 후기 등)
    - 배포 서버 URL(배포했을 경우)
    - 이 외의 내용은 자유롭게 작성 가능
    - 몰아서 하지말고 매일매일 업데이트하기
  
6) Project 고도화 
  - AI를 활용하여 서비스 및 데이터 검색/수집 등 로직 구축

7) 기타
   
  - 최소한 5개 이상의 URL 및 페이지 구성
  - Django REST framework를 사용하는 경우 사용자 요청에 따라 적절한 HTTP response status code를 응답해야 함
  - .gitignore 파일을 추가하여 불필요한 파일 및 폴더 제출 X
  - 필수 요구사항 외 추가 기능 및 반응형 디자인 등 자유롭게 수행

## 선택 요구사항

- 배포
    - 배포 진행은 공용 문서 참고 (https://abit.ly/pb-document)
        - 서버 (Django) 배포
        - 클라이언트(Vue) 배포

## 제출
  1) 학사 시스템
  2) lab ssafy (이름: 10_pjt)
  3) 유의 사항
   - 팀장이 대표로 두 곳 모두 제출
   - 반드시 각 반 담당 강사님 Maintainer로 설정


<br/>

# 2. 역할 분담

## 주요 역할
- 백: `김하연`
- 프론트: `임예원`
  
## 우리만의 분담법
- 첫 프로젝트이기 때문에 역할을 확실히 나누기는 어려울 것 같음
- 주요 역할 대로 분담은 하지만, 각자 부족한 부분들을 보완해 나가며 진행


<br/>

# 3. 프로젝트 설계/기획

## 1) 왜? : 개요 및 주안점
  - 인간은 '관계'를 중요하시 한다는 점에 착안하여 이를 기반으로 한 영화 추천 서비스 기획
    - 시쳇말로 '덕질'도 '덕친(관심사가 같은 친구)'가 있을 때 재밌다!
    `&rarr`  취향이 비슷한 사용자들이 있는 영화 모임(Meet-둥지) 추천 애플리케이션 기획

  - 주안점
    1. 영화 취향을 파악할 수 있는 키워드 생성
    2. 취향이 맞는 사람들이 모인 영화 모임 및 영화 추천
    3. 모임 내 활발한 의견(영화 리뷰) 공유 지향


## 2) 무엇을? : 주요 모델 및 기능
  - Keyword: 개인 취향을 파악하기 위한 키워드
    - 영화 장르, 연대, 국가 필드로 이루어진 키워드 모델 생성
    - 이를 기반으로 취향에 맞는 모임, 영화 추천
    - 하나의 필드에서 여러 개의 키워드 선택 가능, 여러 필드 중 하나만 선택 가능

  - Meet(둥지): 영화 취향이 맞는 사람들이 모인 모임
    - 모임 생성시 모임 성격에 맞는 키워드 선택
    - 이를 기반으로 사용자가 원하는 키워드 필터링해 취향에 맞는 모임 찾을 수 있게 함
    - 생성자가 자동으로 해당 모임 관리자로 설정됨. 관리자만 모임 수정, 삭제 가능

  - Review: 영화에 대한 감상
    - rate: 5점 만점에 0.5점 단위 평가 항목
    - content: 영화에 대한 감상 항목

  - Movie
    - 영화 상세 페이지에선 영화 정보 및 리뷰 제공
    - 선택한 키워드 포함한 영화 구성

  - User
    - 개인 별 선호 키워드 설정 가능

## 3) 어떻게? : 기술적 구현
  - 사용할 기술: Django REST Framework + Vue.js

  - 각자 맡을 업무
    - `김하연`'s 업무
      - 회원가입, 로그인, 로그아웃, 그룹 가입, 그룹 탈퇴, 회원 정보, 영화 정보, 영화 리뷰 생성 및 삭제 기능 구현
    - `임예원`'s 업무
      - 홈, 회원가입, 로그인, 프로필, 영화 정보, 영화 그룹 페이지 생성

  - 추천 알고리즘 구현 및 AI를 통한 고도화
    - 추천 알고리즘(ver 1.0)
      1. Meet(둥지)에 들어가면 해당 Meet 키워드 보유한 영화만 필터링 해 50개 슬라이싱 해 제공

    - AI(chat GPT 4.o)를 통한 기능 고도화(ver 2.0)
      User 키워드 이용와 Movie 평점(vote_average field) 이용해 관련도 정렬
      1. Movie의 키워드와 User 선호 키워드 일치 개수에 따라 영화 정렬
      2. 키워드 일치도 같은 영화는 평점 높은 순으로 정렬
      3. 상위 50개 항목 제공 


  - 사용 API
    - TMDB API
      1. MOVIE LISTS -Top Rated
        : 영화 fixtures 생성용
        - 요청 주소 : "https://api.themoviedb.org/3/movie/top_rated"
        - 사용 항목 : overview, poster_path, title, release_date, vote_average, genre_ids
        - 설정:
          - langauage : ko-KR
          - region : KR

      2. MOVIES - Details
        : top rated api에 없는 영화 별 origin country 추가용
        - 요청 주소 : "https://api.themoviedb.org/3/movie/{movie_id}"
        - 사용 항목 : origin_coutry

  - 최종 ERD
    <img src="DUCK9_ERD(v3).png" />

  - 컴포넌트 구조

  - 전체 레이아웃 구성
  - 전체 테마

<br/>

# 4. 진행 과정
| 날짜       | 공통                                                                                                                                     | front                                                                                       | back                                                                                      | 수정사항                                                      |
|------------|------------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------|---------------------------------------------------------------|
| 2024-05-16 | 컨셉회의 <br> ERD 작성 <br> 컴포넌트 구조 작성  <br> 모델 생성                                                                          | NaN                                                                                         | NaN                                                                                       | NaN                                                           |
| 2024-05-17 | (강사님)프로젝트 컨셉 발표  <br>  movie fixtures 생성 <br>  user fixtures 생성 <br>keyword fixtures 생성 <br>meets fixtures 생성 <br>review fixtues 생성 | 로그인 페이지 생성  <br>  회원가입 페이지 생성  <br>  fixtures loaddata 확인                        | 로그인/로그아웃 구현  <br>  회원가입 구현   <br> TMDB API받아오기                         | NaN                                                           |
| 2024-05-18 | ERD 수정 <br> keyword-user fixtures 생성                                                                                                  | meet 조회 페이지 생성                                                                       | keyword 모델에 era 필드 추가 <br> meet 생성, 수정, 삭제 view 구현                          | NaN                                                           |
| 2024-05-19 | meet모델 수정  <br> user following 필드 생성 <br>                                                                                       | NaN                                                                                         | meet                                                                                      | 1. meet - movie필드 삭제 <br> 2. user follow 테이블 변경       |
| 2024-05-20 | NaN                                                                                                                                      | movie detail 페이지 생성  <br> 좋아요 버튼  구현                                             | NaN                                                                                       | NaN                                                           |
| 2024-05-21 | (강사님)중간 보고                                                                                                                                       | meet detail 비동기 조회 구현  <br>review rate 드래그 별점 구현 <br>url이동 시 스크롤 이동 해결 <br>nav bar 및 footer 수정   <br> review 생성, 수정, 삭제 페이지 생성 | NaN                                                                                       | NaN                                                           |
| 2024-05-22 | NaN                                                                                                                                                     | meet list 이동 효과 추가   <br> 비로그인 사용자 meet 조회 시 영화 조회 개수 수정   <br>                                                                              | NaN                                                                                       | NaN                                                           |
| 2024-05-23 | 발표 자료 제작                                                                                                                                          | NaN                                                                                                                                                                  | NaN                                                                          | NaN                                                           |
| 2024-05-24 | PJT 경진 대회                                                                                                                                           | NaN                                                                                                                                                                  | NaN                                                                          | NaN                                                           |



<br/>

# 5. 초기 계획 및 구현 정도


<br/>

# 6. 소감
`임예원` :
`김하연` :