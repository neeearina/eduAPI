import json

import session

all_data = {}
my_session = session.Session()

for table in session.metadata.sorted_tables:
    table_data = []
    for row in my_session.query(table).all():
        table_data.append({column.name: getattr(row, column.name) for column in table.columns})
    all_data[table.name] = table_data

with open('../fixtures/data.json', 'w', encoding="utf-8") as file:
    json.dump(all_data, file, ensure_ascii=False)
