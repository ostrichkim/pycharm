"""
초기에 group_classification으로 DB 생성, 월별 데이터 파일을 DB에 삽입
데이터 형식(스키마)이 변경될 경우에만 사용
이후부터는 UPDATE를 사용
"""

import csv, sqlite3

#SQL DB 생성
conn = sqlite3.connect('C:\\Users\\KAMA13\\china_car_mkt.sql')
curs = conn.cursor()

#분류테이블 및 스키마 생성
curs.execute("CREATE TABLE IF NOT EXISTS classification ("
             "company_n TEXT PRIMARY KEY, group_name TEXT, nation TEXT"
             ");")

#CSV 파일 열어서 테이블에 분류데이터 INSERT
with open('C:\\Users\\KAMA13\\group_classification.csv', 'r', encoding='utf-8') as classification:
    reader = csv.reader(classification)
    for row in reader:
        to_db = [row[0], row[1], row[2]]
        curs.execute("INSERT INTO classification (company_n, group_name, nation)"
                     "VALUES (?, ?, ?);", to_db)
# INSERT, UPDATE, DELETE문에서는 auto commit이 아니라서 fetchall() 안됨. 아래 코드로 commit 해줘야 db에 반영됨
conn.commit()

#raw_data 테이블 및 스키마 생성
car_schema = "CREATE TABLE IF NOT EXISTS cars (" \
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

conn.close()