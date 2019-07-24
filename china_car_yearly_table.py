import csv, sqlite3

wk_dir = 'C:\\Users\\KAMA13\\china_car\\'

# SQL DB 접근
conn = sqlite3.connect('{0}china_car.sql'.format(wk_dir))
curs = conn.cursor()

while True:
    try:
        year = int(input("Which year is it?"))
        if year > 1900 and year < 3000:
            break
    except TypeError:
        print("Please type an integer greater than 1900 and lesser than 3000.")

# 임시 테이블 청소하기
clr = "DROP TABLE IF EXISTS combined;"
curs.execute(clr)
clr = "DROP TABLE IF EXISTS top1;"
curs.execute(clr)
clr = "DROP TABLE IF EXISTS top2;"
curs.execute(clr)
clr = "DROP TABLE IF EXISTS copied;"
curs.execute(clr)

# 전년도와 당해년도 상위 25개그룹(당해기준)의 연간 판매합계를 combined 테이블에 조인
top25 = "CREATE TABLE top1 AS SELECT group_name, (S1+S2+S3+S4+S5+S6+S7+S8+S9+S10+S11+S12) " \
        "FROM (SELECT nation, group_name, company_n, company, " \
        "make_brand, type, segment, model, year, SUM(M1) AS S1, SUM(M2) AS S2, SUM(M3) AS S3, SUM(M4) AS S4, " \
        "SUM(M5) AS S5, SUM(M6) AS S6, SUM(M7) AS S7, SUM(M8) AS S8, SUM(M9) AS S9, SUM(M10) AS S10, SUM(M11) AS S11, " \
        "SUM(M12) AS S12 FROM cars2 WHERE year = {0} AND group_name IS NOT NULL GROUP BY group_name ORDER BY " \
        "SUM(M1+M2+M3+M4+M5+M6+M7+M8+M9+M10+M11+M12) DESC LIMIT 25) ORDER BY nation;".format(year - 1)
curs.execute(top25)

top25 = "CREATE TABLE top2 AS SELECT nation, group_name, (S1+S2+S3+S4+S5+S6+S7+S8+S9+S10+S11+S12) " \
        "FROM (SELECT nation, group_name, company_n, company, " \
        "make_brand, type, segment, model, year, SUM(M1) AS S1, SUM(M2) AS S2, SUM(M3) AS S3, SUM(M4) AS S4, " \
        "SUM(M5) AS S5, SUM(M6) AS S6, SUM(M7) AS S7, SUM(M8) AS S8, SUM(M9) AS S9, SUM(M10) AS S10, SUM(M11) AS S11, " \
        "SUM(M12) AS S12 FROM cars2 WHERE year = {0} AND group_name IS NOT NULL GROUP BY group_name ORDER BY " \
        "SUM(M1+M2+M3+M4+M5+M6+M7+M8+M9+M10+M11+M12) DESC LIMIT 25) ORDER BY nation;".format(year)
curs.execute(top25)

top25 = "CREATE TABLE combined AS SELECT * FROM top2 LEFT JOIN top1 on top2.group_name = top1.group_name;"
curs.execute(top25)

# 2008년까지(최초 데이터) 각 해의 상위 25개그룹(당해기준)의 연간 판매합계를 combined 테이블에 조인
cursor_year = year - 2
while cursor_year > 2007:
    clr = "DROP TABLE IF EXISTS top1;"
    curs.execute(clr)

    top25 = "CREATE TABLE top1 AS SELECT group_name, (S1+S2+S3+S4+S5+S6+S7+S8+S9+S10+S11+S12) " \
            "FROM (SELECT nation, group_name, company_n, company, " \
            "make_brand, type, segment, model, year, SUM(M1) AS S1, SUM(M2) AS S2, SUM(M3) AS S3, SUM(M4) AS S4, " \
            "SUM(M5) AS S5, SUM(M6) AS S6, SUM(M7) AS S7, SUM(M8) AS S8, SUM(M9) AS S9, SUM(M10) AS S10, SUM(M11) AS S11, " \
            "SUM(M12) AS S12 FROM cars2 WHERE year = {0} AND group_name IS NOT NULL GROUP BY group_name ORDER BY " \
            "SUM(M1+M2+M3+M4+M5+M6+M7+M8+M9+M10+M11+M12) DESC LIMIT 25) ORDER BY nation;".format(cursor_year)
    curs.execute(top25)

    # combined 테이블에 overwrite이 불가능하므로 임시테이블 copied 생성
    overwrite = "CREATE TABLE copied AS SELECT * FROM combined;"
    curs.execute(overwrite)

    clr = "DROP TABLE combined;"
    curs.execute(clr)

    top25 = "CREATE TABLE combined AS SELECT * FROM copied LEFT JOIN top1 on copied.group_name = top1.group_name;"
    curs.execute(top25)

    clr = "DROP TABLE copied;"
    curs.execute(clr)

    cursor_year -= 1

top25 = "SELECT * FROM combined;"
curs.execute(top25)
rslt = curs.fetchall()


# Header 달기
new_result = []
for row in rslt:
    row_list = list(row)
    row = row_list[:2] + row_list[2::2]
    new_result.append(row)

num_year = len(new_result[0])-2
header1 = ['nation','group_name']
for y in range(num_year):
    header1.append('{0}'.format(year-y))

# 쿼리 저장
with open('{0}china_car_yearly_table.csv'.format(wk_dir), 'w', encoding='utf-8', newline='') as table_csv:
    writer = csv.writer(table_csv)
    writer.writerow(header1)
    writer.writerows(new_result)
    writer.writerow('\n')
