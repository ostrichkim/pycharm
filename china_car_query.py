import csv, sqlite3

wk_dir = 'C:\\Users\\KAMA13\\china_car\\'

# SQL DB 접근
conn = sqlite3.connect('{0}china_car.sql'.format(wk_dir))
curs = conn.cursor()

# column 이름 나열
curs.execute('PRAGMA TABLE_INFO(cars2)')
labels = [tup[1] for tup in curs.fetchall()]

year = int(input("Select year: "))
select_month = int(input("Select month (For yearly data, type 12): "))


clr = "DROP TABLE IF EXISTS top1"
curs.execute(clr)
clr = "DROP TABLE IF EXISTS top2"
curs.execute(clr)

top25 = "CREATE TABLE top1 AS SELECT * FROM (SELECT nation, group_name, company_n, company, make_brand, type, segment, model, year, SUM(M1), " \
        "SUM(M2), SUM(M3), SUM(M4), SUM(M5), SUM(M6), SUM(M7), SUM(M8), SUM(M9), SUM(M10), SUM(M11), SUM(M12) FROM cars2 " \
        "WHERE year = {0} AND group_name IS NOT NULL GROUP BY group_name ORDER BY SUM(M1+M2+M3+M4+M5+M6+M7+M8+M9+M10+M11+M12) " \
        "DESC LIMIT 25) ORDER BY nation;".format(year - 1)
curs.execute(top25)
by_company_n_last = curs.fetchall()

top25 = "CREATE TABLE top2 AS SELECT * FROM (SELECT nation, group_name, company_n, company, make_brand, type, segment, model, year, SUM(M1), " \
        "SUM(M2), SUM(M3), SUM(M4), SUM(M5), SUM(M6), SUM(M7), SUM(M8), SUM(M9), SUM(M10), SUM(M11), SUM(M12) FROM cars2 " \
        "WHERE year = {0} AND group_name IS NOT NULL GROUP BY group_name ORDER BY SUM(M1+M2+M3+M4+M5+M6+M7+M8+M9+M10+M11+M12) " \
        "DESC LIMIT 25) ORDER BY nation;".format(year)
curs.execute(top25)
by_company_n_current = curs.fetchall()

top25 = "SELECT * FROM top2 LEFT JOIN top1 on top2.group_name = top1.group_name;"
curs.execute(top25)
by_company_n_join = curs.fetchall()


# top25 당해연도와 전년도 분리
new_last = []
new_current = []
final_last = []
final_current = []

for row in by_company_n_join:
    row_list = list(row)
    new_last.append(row_list[21:])
    new_current.append(row_list[:21])

# 전년 월별 합계
for row in new_last:
    cumulative = 0
    for a in range(9, 9 + select_month):
        # 금년에 따라 top25를 뽑았기 때문에 값이 없는 열이 있으므로 row[a]가 존재하는지 확인
        if row[a]:
            cumulative += row[a]
    row_list = list(row)
    row = [row_list[0], row_list[1], row_list[5], row_list[8], row_list[8 + select_month], "", cumulative, ""]
    final_last.append(row)

# 금년 월별 합계
for row in new_current:
    cumulative = 0
    for a in range(9, 9 + select_month):
        cumulative += row[a]
    row_list = list(row)
    row = [row_list[0], row_list[1], row_list[5], row_list[8], row_list[8 + select_month], "", cumulative, ""]
    final_current.append(row)


# 원하는 데이터 뽑기함수
def query(year, condition, group_by):
    qry = "SELECT nation, group_name, company_n, company, make_brand, type, segment, model, year, SUM(M1), SUM(M2), " \
          "SUM(M3), SUM(M4), SUM(M5), SUM(M6), SUM(M7), SUM(M8), SUM(M9), SUM(M10), SUM(M11), SUM(M12) FROM cars2 " \
          "WHERE year = {0} {1} GROUP BY {2};".format(year, condition, group_by)
    curs.execute(qry)
    result = curs.fetchall()

    # 월별로 합계구해서 뽑아내기
    new_result = []
    final_result = []
    for row in result:
        cumulative = 0
        for a in range(9, 9 + select_month):
            cumulative += row[a]
        row_list = list(row)
        row_list.append(cumulative)
        row = row_list[:9]
        row.append(row_list[8 + select_month])
        row.append(row_list[-1])
        new_result.append(row)

    # column 합계 구하기
    month_sum = 0
    cumulative_sum = 0
    for row in new_result:
        month_sum += row[9]
        cumulative_sum += row[10]
    new_result.append(['total','','','','','','','','',month_sum,cumulative_sum])

    # 비중 구하기
    for row_list in new_result:
        month_share = round(row_list[9] / month_sum * 100, 1)
        cumulative_share = round(row_list[10] / cumulative_sum * 100, 1)
        row = [row_list[0], row_list[1], row_list[5], row_list[8], row_list[9], month_share, row_list[10], cumulative_share]
        final_result.append(row)

    return final_result

by_nation_last = query(year-1, '', 'nation')
by_nation_current = query(year, '', 'nation')
by_type_last = query(year-1, '', 'type')
by_type_current = query(year, '', 'type')


labels_modified = [labels[0], labels[1], labels[5], labels[8], "M" + str(select_month), "Month Share", "Cumulative Total", "Cumulative Share"]
# 첫번째 쿼리 저장(스키마와 상위 25개 업체 total, 그리고 처음 선택 쿼리)
with open('{0}china_car_query.csv'.format(wk_dir), 'w', encoding='utf-8', newline='') as query_csv:
    writer = csv.writer(query_csv)
    writer.writerow(labels_modified)
    writer.writerows(final_last)
    writer.writerow('\n')
    writer.writerows(final_current)
    writer.writerow('\n')
    writer.writerow('By Nation')
    writer.writerows(by_nation_last)
    writer.writerow('\n')
    writer.writerows(by_nation_current)
    writer.writerow('\n')
    writer.writerow('By Type')
    writer.writerows(by_type_last)
    writer.writerow('\n')
    writer.writerows(by_type_current)


cont = input("Do you want to continue? (Y/N): ")

# 원하는 만큼 쿼리 계속 날리기
while cont == 'Y':
    condition = input("Any condition? (ex: ,nation = china, group_name = BYD): ")
    group_by = input("Group by which category? (nation, group_name, company_n, company, make_brand, type, segment, model): ")
    add_query_last = query(year-1, condition, group_by)
    add_query_current = query(year, condition, group_by)

    with open('{0}china_car_query.csv'.format(wk_dir), 'a', encoding='utf-8', newline='') as query_add:
        writer = csv.writer(query_add)
        writer.writerow('\n')
        writer.writerows(add_query_last)
        writer.writerow('\n')
        writer.writerows(add_query_current)

    cont = input("Do you want to continue? (Y/N): ")