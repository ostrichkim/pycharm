"""
raw data는 1개년도 월별로만 데이터 뽑아옴
맨 첫번째 행을 삭제해서 2019.csv로 저장하고 아래 코드 돌리기
"""

import csv, sqlite3, re

wk_dir = 'C:\\Users\\KAMA13\\china_car\\'

# SQL DB 접근
conn = sqlite3.connect('{0}china_car.sql'.format(wk_dir))
curs = conn.cursor()

# 분류테이블 및 스키마 생성(계속 수정해야 하니까 표를 drop했다가 create)
curs.execute("DROP TABLE IF EXISTS classification")
curs.execute("CREATE TABLE classification ("
             "company_n TEXT PRIMARY KEY, group_name TEXT, nation TEXT);")

# CSV 파일 열어서 테이블에 분류데이터 INSERT
with open('{0}group_classification.csv'.format(wk_dir), 'r', encoding='utf-8') as classification:
    reader = csv.reader(classification)
    for row in reader:
        to_db = [row[0], row[1], row[2]]
        curs.execute("INSERT INTO classification (company_n, group_name, nation)"
                     "VALUES (?, ?, ?);", to_db)

# INSERT, UPDATE, DELETE문에서는 auto commit이 아니라서 fetchall() 안됨. 아래 코드로 commit 해줘야 db에 반영됨
conn.commit()

# 다운받은 raw data(csv) 열어서 preprocessing 후 저장
year = input("Type current year: ")
with open('{0}{1}.csv'.format(wk_dir, year), 'r', encoding='utf-8') as cars:
    reader = csv.reader(cars)
    new = []

    for row in reader:
        # 수치가 들어간 column에서 '-'와 'N/A' 표시를 모두 '0'으로 변경. 음수값은 양수값으로 변환
        for a in range(6, len(row)-2):
            if row[a] == '-' or row[a] == 'N/A':
                row[a] = 0
            else:
                row[a] = abs(int(row[a]))

        # niou 등 특수문자를 제거. 전부 한글/숫자/알파벳으로 변경
        row[5] = re.sub('[^가-힝0-9a-zA-Z\\s]', '', row[5])

        # 승용만 골라서 맨 끝 column 빼고, 첫번째 column은 해당 year로 바꿔서 저장
        if row[3] == 'Sedan/Hatchback' or row[3] == 'SUV' or row[3] == 'MPV' or row[3] == 'Mini Van':
            row[0] = year
            new.append(row[:-1])

    # 새 csv 파일 "china_car"로 저장
    with open('{0}china_car.csv'.format(wk_dir), 'w', encoding='utf-8', newline='') as new_cars:
        writer = csv.writer(new_cars)
        writer.writerows(new)


# raw_data 테이블, 스키마 생성
car_schema = "CREATE TABLE IF NOT EXISTS cars (" \
             "year INTEGER, company TEXT, make_brand TEXT, type TEXT, segment TEXT, model TEXT, " \
             "M1 INTEGER, M2 INTEGER, M3 INTEGER, M4 INTEGER, M5 INTEGER, M6 INTEGER, M7 INTEGER," \
             "M8 INTEGER, M9 INTEGER, M10 INTEGER, M11 INTEGER, M12 INTEGER, company_n TEXT NOT NULL);"
curs.execute(car_schema)
index_set = "CREATE UNIQUE INDEX IF NOT EXISTS idx ON cars(year, company, make_brand, type, segment, model, company_n);"
curs.execute(index_set)

# CSV 파일 열어서 테이블에 raw_data INSERT or REPLACE
with open('{0}china_car.csv'.format(wk_dir), 'r', encoding='utf-8') as cars:
    reader = csv.reader(cars)
    for row in reader:
        to_db = [row[x] for x in range(19)]
        curs.execute("INSERT OR REPLACE INTO cars (year, company, make_brand, type, segment, model,"
                     "M1, M2, M3, M4, M5, M6, M7, M8, M9, M10, M11, M12, company_n)"
                     "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);", to_db)
conn.commit()

# Rollback 옵션
rollback = input("Would you like to revert the inserted data? (Y/N): ")
if rollback == "Y":
    curs.execute("DELETE FROM cars WHERE year = {0}".format(year))
    conn.commit()
    print("Your data for the year of %s was reverted." % year)

# SQL DB로 raw_data와 group classification LEFT JOIN해서 데이터를 cars2 테이블로 저장(기존 cars2 테이블은 삭제)
clr = "DROP TABLE IF EXISTS cars2"
curs.execute(clr)

cars2 = "CREATE TABLE cars2 AS SELECT nation, group_name, cars.company_n, company, make_brand, type, segment, model," \
        "year, M1, M2, M3, M4, M5, M6, M7, M8, M9, M10, M11, M12 FROM cars " \
        "LEFT JOIN classification ON cars.company_n = classification.company_n;"
curs.execute(cars2)


# company에 따라 group_name이 나뉘는 애들(cars.company_n)
# FAW Car; Jiangxi Jiangling Holdings Ltd.; Jiangxi Changhe Suzuki Automobile (2014-); Zhengzhou Nissan Automobile
set_category = 'group_name'
where_category = 'company'

def update(set_name, where_name):
    upt = "UPDATE cars2 SET {0} = '{1}' WHERE {0} IS NULL AND ({2} = '{3}');".format(set_category, set_name, where_category, where_name)
    curs.execute(upt)
    conn.commit()

update('Mazda', 'Mazda')
update('Nissan', 'Renault-Nissan Alliance')
update('Suzuki', 'Suzuki')
update('Mitsubishi', 'Mitsubishi')
update('Ford', 'Ford Group')
update('Daimler', 'Daimler Group')
update('FCA', 'FCA')
update('Dongfeng', 'Dongfeng (Dongfeng Motor Corp.)')
update('JMC', 'Jiangling Motors Co. Group')
update('FAW', 'FAW (China FAW Group Corp.)')
update('Geely Holding', 'Geely Holding Group')
update('BAIC', 'BAIC Group')

# group_name에 따라 nation 분류
set_category = 'nation'
where_category = 'group_name'
update('japan', 'Mazda')
update('japan', 'Nissan')
update('japan', 'Suzuki')
update('japan', 'Mitsubishi')
update('us', 'Ford')
update('europe', 'Daimler')
update('europe', 'FCA')
update('china', 'Dongfeng')
update('china', 'JMC')
update('china', 'FAW')
update('china', 'Geely Holding')
update('china', 'BAIC')

# 분류 안되는 애들 nation은 china로
where_category = 'company'
update('china', ' Small and Medium OEM')
update('china', 'Other/Adjustment')
update('china', 'N/A')

# nation에 분류되지 않는 신규회사가 있으면 작업중단, 없으면 계속 고
curs.execute("SELECT group_name, company_n, company, make_brand FROM cars2 WHERE nation IS NULL;")
check = curs.fetchall()

if check:
    print("***There are some unclassified companies. Please modify the classification table.\n(group_name, company_n, company, make_brand)")
    print(check)
    quit()

conn.close()