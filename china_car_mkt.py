import csv, sqlite3

"""
다운받은 raw data(csv) 열어서 preprocessing 후 저장
"""

with open('C:\\Users\\KYJ\\china_car_mkt.csv', 'r', encoding='utf-8') as cars:
    reader = csv.reader(cars)
    new = []
    count = 0
    for row in reader:
        for a in range(6,len(row)-1):
            if row[a] == '-' or row[a] == 'N/A':
                row[a] = 0
            else:
                row[a] = int(row[a])
        row[0] = count
        count += 1
        print(row)
        new.append(row)
    new[0][0] = "Index"
    new[0][-2] = "Group_name"

    with open('C:\\Users\\KYJ\\china_car_mkt_edited.csv', 'w', encoding='utf-8', newline='') as new_cars:
        writer = csv.writer(new_cars)
        writer.writerows(new[1:len(new)-1])

"""
raw data로 SQL DB 생성
"""

#SQL DB 생성하고 작업시작
conn = sqlite3.connect('C:\\Users\\KYJ\\china_car_mkt.sql')
curs = conn.cursor()

#테이블 및 스키마 생성
curs.execute("CREATE TABLE cars ("
             "id INTEGER PRIMARY KEY, company TEXT, make_brand TEXT, type TEXT, segment TEXT, model TEXT,"
             "Y2011 INTEGER, Y2012 INTEGER, Y2013 INTEGER, Y2014 INTEGER, Y2015 INTEGER, Y2016 INTEGER, company_n TEXT"
             ");")

#CSV 파일 열어서 테이블에 데이터 INSERT
with open('C:\\Users\\KYJ\\china_car_mkt_edited.csv', 'r', encoding='utf-8') as cars:
    reader = csv.reader(cars)
    for row in reader:
        to_db = [row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12]]
        curs.execute("INSERT INTO cars (id, company, make_brand, type, segment, model, Y2011, Y2012, Y2013, Y2014, Y2015, Y2016, company_n)"
                     "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);", to_db)

# INSERT, UPDATE, DELETE문에서는 auto commit이 아니라서 fetchall() 안됨. 아래 코드로 commit 해줘야 db에 반영됨
conn.commit()

#DB에서 수행한 작업 모두 result에 저장, csv 파일로 export
curs.execute("SELECT * FROM cars")
result = curs.fetchall()
with open('C:\\Users\\KYJ\\china_car_mkt_final.csv', 'w', encoding='utf-8', newline='') as new_cars:
    writer = csv.writer(new_cars)
    writer.writerows(result)


#DB 닫기
conn.close()