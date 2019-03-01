import csv, sqlite3, re

#다운받은 raw data(csv) 열어서 preprocessing 후 저장

with open('C:\\Users\\KAMA13\\raw_data.csv', 'r', encoding='utf-8') as cars:
    reader = csv.reader(cars)
    new = []
    idx = 1

    for row in reader:
        # model에서 특수문자와 공백 제거 -> 애초에 파일을 utf-8로 열 때 특수문자 인식을 못해서 column이 하나씩 밀림...
        # row[5] = re.sub('\W', '', row[5])

        # 수치가 들어간 column에서 '-'와 'N/A' 표시를 모두 '0'으로 변경
        for a in range(6, len(row)-2):
            if row[a] == '-' or row[a] == 'N/A':
                row[a] = 0
            else:
                row[a] = abs(int(row[a]))

        # 승용만 골라서 맨 끝 column 빼고, 첫번째 column은 인덱스로 바꿔서 저장
        if row[3] == 'Sedan/Hatchback' or row[3] == 'SUV' or row[3] == 'MPV' or row[3] == 'Mini Van':
            row[0] = idx
            idx += 1
            new.append(row[:-1])

    # 새 csv 파일로 저장
    with open('C:\\Users\\KAMA13\\china_car_mkt.csv', 'w', encoding='utf-8', newline='') as new_cars:
        writer = csv.writer(new_cars)
        writer.writerows(new)


# SQL DB 접근
conn = sqlite3.connect('C:\\Users\\KAMA13\\china_car_mkt.sql')
curs = conn.cursor()

#raw_data 테이블 및 스키마 생성
curs.execute("DROP TABLE IF EXISTS cars")
car_schema = "CREATE TABLE cars (" \
             "id INTEGER PRIMARY KEY, company TEXT, make_brand TEXT, type TEXT, segment TEXT, model TEXT, " \
             "L1 INTEGER, L2 INTEGER, L3 INTEGER, L4 INTEGER, L5 INTEGER, L6 INTEGER, L7 INTEGER, L8 INTEGER, L9 INTEGER, L10 INTEGER, L11 INTEGER, L12 INTEGER, " \
             "C1 INTEGER, C2 INTEGER, C3 INTEGER, C4 INTEGER, C5 INTEGER, C6 INTEGER, C7 INTEGER, C8 INTEGER, C9 INTEGER, C10 INTEGER, C11 INTEGER, C12 INTEGER, " \
             "company_n TEXT NOT NULL);"
curs.execute(car_schema)

#CSV 파일 열어서 테이블에 raw_data INSERT
with open('C:\\Users\\KAMA13\\china_car_mkt.csv', 'r', encoding='utf-8') as cars:
    reader = csv.reader(cars)
    for row in reader:
        to_db = [row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12], row[13], row[14], row[15], row[16],
                 row[17], row[18], row[19], row[20], row[21], row[22], row[23], row[24], row[25], row[26], row[27], row[28], row[29], row[30]]
        curs.execute("INSERT INTO cars (id, company, make_brand, type, segment, model, L1, L2, L3, L4, L5, L6, L7, L8, L9, L10,"
                     " L11, L12, C1, C2, C3, C4, C5, C6, C7, C8, C9, C10, C11, C12, company_n)"
                     "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);", to_db)
conn.commit()

# SQL DB로 raw_data와 classification LEFT JOIN해서 데이터를 cars2 테이블로 저장
clr = "DROP TABLE IF EXISTS cars2"
curs.execute(clr)

cars2 = "CREATE TABLE cars2 AS SELECT nation, group_name, cars.company_n, company, make_brand, type, model, L1, L2, L3, L4, L5, L6, L7, L8, L9, L10, L11, L12, C1, C2, C3, C4, C5, C6, C7, C8, C9, C10, C11, C12 " \
      "FROM cars LEFT JOIN classification ON cars.company_n = classification.company_n;"
curs.execute(cars2)

# nation이 null이면 company 또는 company_n에 따라 nation 값 삽입
upt = "UPDATE cars2 SET nation = 'japan' WHERE nation IS NULL AND (company = 'Suzuki' OR company = 'Mazda' OR company_n = 'Beijing New Energy Vehicle (BJEV)/Dongfeng Nissan Passenger Vehicle/n.a.');"
curs.execute(upt)
conn.commit()

upt = "UPDATE cars2 SET nation = 'china' WHERE nation IS NULL AND (company = 'Geely Holding Group' OR company = 'Mazda' OR company = 'FAW (China FAW Group Corp.)'" \
      "OR company = 'Anhui Jianghuai Automotive Group' OR company = 'BAIC Group' OR company = 'Fujian Motor Industrial Group Co. (FJMG)' OR company = ' Small and Medium OEM'" \
      "OR company_n = 'FAW Haima Automobile/n.a.');"
curs.execute(upt)
conn.commit()

curs.execute("SELECT group_name, company_n, company, make_brand FROM cars2 WHERE nation IS NULL;")
check = curs.fetchall()

# nation에 분류되지 않는 신규회사가 있으면 작업중단, 없으면 계속 고
# 문제!!!!!!! Beijing New Energy Vehicle (BJEV)/Dongfeng Nissan Passenger Vehicle/n.a. 이건 왜 missing 되지??
if check:
    print("***There are some unclassified companies. (group_name, company_n, company, make_brand)")
    print(check)
    quit()

# JOIN하고 preprocessing 모두 끝낸 결과를 result에 저장, csv 파일로 export
curs.execute("SELECT * FROM cars2;")
result = curs.fetchall()

with open('C:\\Users\\KAMA13\\china_car_mkt_result.csv', 'w', encoding='utf-8', newline='') as new_cars:
    writer = csv.writer(new_cars)
    writer.writerows(result)

# column 이름 나열
curs.execute('PRAGMA TABLE_INFO(cars2)')
labels = [tup[1] for tup in curs.fetchall()]

# 여기서부터는 원하는 데이터 뽑기
curs.execute("SELECT nation, group_name, company_n, company, make_brand, type, model, SUM(L1), SUM(L2), SUM(L3), SUM(L4), SUM(L5), SUM(L6), SUM(L7), SUM(L8), SUM(L9), SUM(L10), SUM(L11), SUM(L12), "
             "SUM(C1), SUM(C2), SUM(C3), SUM(C4), SUM(C5), SUM(C6), SUM(C7), SUM(C8), SUM(C9), SUM(C10), SUM(C11), SUM(C12) FROM cars2 GROUP BY nation;")
by_nation = curs.fetchall()
curs.execute("SELECT nation, group_name, company_n, company, make_brand, type, model, SUM(L1), SUM(L2), SUM(L3), SUM(L4), SUM(L5), SUM(L6), SUM(L7), SUM(L8), SUM(L9), SUM(L10), SUM(L11), SUM(L12),"
             "SUM(C1), SUM(C2), SUM(C3), SUM(C4), SUM(C5), SUM(C6), SUM(C7), SUM(C8), SUM(C9), SUM(C10), SUM(C11), SUM(C12) FROM cars2 GROUP BY group_name "
             "ORDER BY SUM(C1+C2+C3+C4+C5+C6+C7+C8+C9+C10+C11+C12) DESC LIMIT 25;")
by_company_n = curs.fetchall()
curs.execute("SELECT nation, group_name, company_n, company, make_brand, type, model, SUM(L1), SUM(L2), SUM(L3), SUM(L4), SUM(L5), SUM(L6), SUM(L7), SUM(L8), SUM(L9), SUM(L10), SUM(L11), SUM(L12),"
             "SUM(C1), SUM(C2), SUM(C3), SUM(C4), SUM(C5), SUM(C6), SUM(C7), SUM(C8), SUM(C9), SUM(C10), SUM(C11), SUM(C12) FROM cars2 GROUP BY type;")
by_type = curs.fetchall()

with open('C:\\Users\\KAMA13\\china_car_mkt_query.csv', 'w', encoding='utf-8', newline='') as query:
    writer = csv.writer(query)
    writer.writerow(labels)
    writer.writerows(by_nation)
    writer.writerows("\n")
    writer.writerows(by_company_n)
    writer.writerows("\n")
    writer.writerows(by_type)


"""
#뽑아야 할 테이블 목록
#GROUP BY nation: 당해년도 당월, 전년당월, 그것간 비교, 전월비교, 당해년도 누적, 전년동기, 그것간 비교 (모두 수치와 점유율로)
#GROUP BY company_n ORDER BY 당월 DESC HAVING 당월실적 > 30만대
#나머지 데이터도 같은방식으로 뽑아내고, 같은파일에 추가하기
#참고 : dot command는 sqlite를 직접 실행시 shell에서만 쓸 수 있음. 아래는 dot command로 csv export하는 방법
curs.execute(".header on")
curs.execute(".mode csv")
curs.execute(".output china_car_mkt_result.csv")
curs.execute("SELECT * FROM cars2;")
        for a in range(2, 6):
            row[a] = re.sub('\W', '', row[a])
"""

#DB 닫기
conn.close()