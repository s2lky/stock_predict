# 미국 주가 데이터를 이용한 주가 예측 서비스

---

**프로젝트 기간:** 2023.09.26 ~ 2023.11.03 (6주)

**프로젝트 도구:** AWS EC2, Docker, Airflow, Kafka, Hadoop, Redis, PostgreSQL, Flask, React, Nginx, Github

**사용 언어:** Python, SQL

---

### ****프로젝트 개요****

- 미국 주가 데이터를 이용한 주가 예측 프로젝트

### 프로젝트 배경

- 달러의 가치 상승, 주변에 해외 주식 거래에 대한 관심도가 높아짐에 따라서, 미국 주가 데이터를 예측해 주는 서비스를 만들어보면 어떨까? 라는 생각에서 시작하게 됨

### 프로젝트 아키텍쳐
![Architecture](https://github.com/s2lky/stock_predict/assets/132236456/b22fd5dc-62b2-4e4c-9937-9a85cf26c57d)

### 프로젝트 기술 스택

- **DevOps**
    
    ![Docker](https://img.shields.io/badge/docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
    
- **Database**
    
    ![PostgreSQL](https://img.shields.io/badge/postgresql-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)
    ![Hadoop](https://img.shields.io/badge/apachehadoop-66CCFF?style=for-the-badge&logo=apachehadoop&logoColor=white)
    ![Redis](https://img.shields.io/badge/redis-DC382D?style=for-the-badge&logo=redis&logoColor=white)

- **Data Engineer**

    ![Airflow](https://img.shields.io/badge/apacheairflow-017CEE?style=for-the-badge&logo=apacheairflow&logoColor=white)
    ![Kafka](https://img.shields.io/badge/apachekafka-231F20?style=for-the-badge&logo=apachekafka&logoColor=white)

- **Frontend/Backend**

    ![Flask](https://img.shields.io/badge/flask-000000?style=for-the-badge&logo=flask&logoColor=white)
    ![React](https://img.shields.io/badge/react-61DAFB?style=for-the-badge&logo=react&logoColor=white)
    
  
**Redis 선택 이유**

- 데이터베이스에 들어오는 트래픽을 줄이기 위해서
- 많은 사람들이 검색하는 데이터들을 빠르게 전달하기 위해서

### 개발 인원

| 이름   | 담당 업무                                                                                                                                                                                                 |
|--------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 김동호 | - DB 설계 및 EC2 환경 세팅 |
| 정명균 | - DB 설계, Frontend와 Backend 개발 |
| 정윤재 | - 주가 데이터 수집 및 사용자 데이터 수집, 데이터 적재|
| 허선우 | - 주가 예측을 위한 예측 프로그램 모델링 및 데이터 적재 |

### 프로젝트 진행 과정

1. 주가 데이터 수집 및 적재
2. 주가 데이터 예측을 위한 모델링
3. 웹을 통한 데이터 서빙 

### 프로젝트 구현 내용

1. 주가 데이터 수집 및 적재
![airflow](https://github.com/s2lky/stock_predict/assets/132236456/5339e805-362d-42f4-88c1-d5ebd316859c)

2. 주가 데이터 예측을 위한 모델링
![modeling](https://github.com/s2lky/stock_predict/assets/132236456/a6929b81-61a6-4974-8944-562beb8e542d)

3. 웹을 통한 데이터 서빙
![web_login](https://github.com/s2lky/stock_predict/assets/132236456/aa08fc69-73ff-47ef-b4cb-d941382186f2)
![web_request](https://github.com/s2lky/stock_predict/assets/132236456/293bd7fb-9267-46dc-8b0a-5b4a0fcc427d)

   
### 프로젝트 한계 및 개선 방안

**한계**

- 모델을 돌리는 데 걸리는 시간 및 데이터 수집 시간으로 인해, 조금 더 좋은 성능을 내도록 시간 단위, 분 단위의 데이터를 돌리지 못함

**개선 방안**

- 데이터 수집을 위해서 컨테이너를 여러 개로 나눈 후에 데이터 수집 목록 분산 (현재는 한 컨테이너에서 모든 데이터를 수집하는 중)
- hdfs에 데이터 적재시에 csv형식의 파일을 parquet형식으로 변환 후 적재하는 방법을 통해 데이터의 용량 최소화
