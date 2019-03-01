import csv, sqlite3

wk_dir = 'C:\\Users\\KAMA13\\china_car\\'

# SQL DB 접근
conn = sqlite3.connect('{0}china_car.sql'.format(wk_dir))
curs = conn.cursor()

# column 이름 나열
curs.execute('PRAGMA TABLE_INFO(cars2)')
labels = [tup[1] for tup in curs.fetchall()]

year = int(input("Which year?"))

# 전년 group_name 중 상위 25개 뽑기
top25 = "SELECT * FROM (SELECT nation, group_name, company_n, company, make_brand, type, segment, model, year, SUM(M1), " \
        "SUM(M2), SUM(M3), SUM(M4), SUM(M5), SUM(M6), SUM(M7), SUM(M8), SUM(M9), SUM(M10), SUM(M11), SUM(M12) FROM cars2 " \
        "WHERE year = {0} AND group_name IS NOT NULL GROUP BY group_name ORDER BY SUM(M1+M2+M3+M4+M5+M6+M7+M8+M9+M10+M11+M12) " \
        "DESC LIMIT 25) ORDER BY nation;".format(year - 1)
curs.execute(top25)
by_company_n_last = curs.fetchall()

# 금년 group_name 중 상위 25개 뽑기
top25 = "SELECT * FROM (SELECT nation, group_name, company_n, company, make_brand, type, segment, model, year, SUM(M1), " \
        "SUM(M2), SUM(M3), SUM(M4), SUM(M5), SUM(M6), SUM(M7), SUM(M8), SUM(M9), SUM(M10), SUM(M11), SUM(M12) FROM cars2 " \
        "WHERE year = {0} AND group_name IS NOT NULL GROUP BY group_name ORDER BY SUM(M1+M2+M3+M4+M5+M6+M7+M8+M9+M10+M11+M12) " \
        "DESC LIMIT 25) ORDER BY nation;".format(year)
curs.execute(top25)
by_company_n_current = curs.fetchall()

# 원하는 데이터 뽑기함수
def query():
    select_month = int(input("Select month (For yearly data, type 12): "))
    condition = input("Any condition? (ex: ,nation = china, group_name = BYD): ")
    group_by = input("Group by which category? (nation, group_name, company_n, company, make_brand, type, segment, model): ")
    qry = "SELECT nation, group_name, company_n, company, make_brand, type, segment, model, year, SUM(M1), SUM(M2), " \
          "SUM(M3), SUM(M4), SUM(M5), SUM(M6), SUM(M7), SUM(M8), SUM(M9), SUM(M10), SUM(M11), SUM(M12) FROM cars2 " \
          "WHERE year = {0} {1} GROUP BY {2};".format(year, condition, group_by)
    curs.execute(qry)
    result = curs.fetchall()

    # 월별로 합계구해서 뽑아내기
    new_result = []
    final_result = []
    for row in result:
        cumultative = 0
        for a in range(9, 9 + select_month):
            cumultative += row[a]
        row_list = list(row)
        row_list.append(cumultative)
        row = row_list[:9]
        row.append(row_list[8 + select_month])
        row.append(row_list[-1])
        new_result.append(row)

    # column 합계 구하기
    month_sum = 0
    cumultative_sum = 0
    for row in new_result:
        month_sum += row[9]
        cumultative_sum += row[10]

    new_result.append(['total','','','','','','','','',month_sum,cumultative_sum])

    # 비중 구하기
    for row in new_result:
        month_share = round(row[9] / month_sum * 100, 1)
        cumultative_share = round(row[10] / cumultative_sum * 100, 1)
        row.insert(10, month_share)
        row.append(cumultative_share)
        final_result.append(row)

    return final_result

rslt = query()

# 첫번째 쿼리 저장(스키마와 상위 25개 업체 total, 그리고 처음 선택 쿼리)
with open('{0}china_car_query.csv'.format(wk_dir), 'w', encoding='utf-8', newline='') as query_csv:
    writer = csv.writer(query_csv)
    writer.writerow(labels)
    writer.writerows(by_company_n_last)
    writer.writerow('\n')
    writer.writerows(by_company_n_current)
    writer.writerow('\n')
    writer.writerows(rslt)

cont = input("Do you want to continue?(Y/N): ")

# 원하는 만큼 쿼리 계속 날리기
while cont == 'Y':
    add_query = query()

    with open('{0}china_car_query.csv'.format(wk_dir), 'a', encoding='utf-8', newline='') as query_add:
        writer = csv.writer(query_add)
        writer.writerow('\n')
        writer.writerows(add_query)

    cont = input("Do you want to continue?(Y/N): ")

"""
#뽑아야 할 테이블 목록
#GROUP BY nation: 당해년도 당월, 전년당월, 그것간 비교, 전월비교, 당해년도 누적, 전년동기, 그것간 비교 (모두 수치와 점유율로)
#GROUP BY company_n ORDER BY 당월 LIMIT 당월실적 상위 25개 업체
#나머지 데이터도 같은방식으로 뽑아내고, 같은파일에 추가하기
"""