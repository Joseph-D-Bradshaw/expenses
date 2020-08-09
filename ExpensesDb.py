import sqlite3
from typing import List, Tuple

class ExpensesDb:

    def __init__(self):
        self.conn = sqlite3.connect('expenses.db')
        self.cursor = self.conn.cursor()

        if 'expenses' not in self._table_names:
            self.create_expenses_table()

    @property
    def all_expenses(self) -> List[any]:
        query = "SELECT * FROM expenses"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    @property
    def expenses_columns(self) -> List[Tuple]:
        self.cursor.execute("PRAGMA TABLE_INFO(expenses)")
        results = self.cursor.fetchall()
        return [(row[1], row[2]) for row in results]

    @property
    def _table_names(self) -> List[str]:
       self.cursor.execute('SELECT name FROM sqlite_master WHERE type="table"')
       table_names = self.cursor.fetchall()
       table_names = [x[0] for x in table_names]
       return table_names


    def create_expenses_table(self) -> bool:
        success = True
        create_table_q = """CREATE TABLE expenses (
                        id INTEGER PRIMARY KEY,
                        expense_name TEXT NOT NULL,
                        categories TEXT NOT NULL,
                        cost REAL NOT NULL,
                        date datetime NOT NULL);"""
        try:
            self.cursor.execute(create_table_q)
            self.conn.commit()
        except Exception as e:
            print("Error occured when creating table", e)
            success = False
        return success


    def add_record(self, expense_name: str, categories: List[str], cost: float, date: str):
        # TODO: Ensure string is valid date and do validation on parameters
        insert_q = f"""INSERT INTO expenses
                    (expense_name, categories, cost, date)
                    VALUES ('{expense_name}', '{self._parse_list(categories)}', {cost}, '{date}')"""
        self.cursor.execute(insert_q)
        self.conn.commit()
    

    def _parse_list(self, to_clean: List[str]) -> str:
        to_clean = str(to_clean)
        to_clean = to_clean.replace("'", "")
        to_clean = to_clean.replace("[", "")
        to_clean = to_clean.replace("]", "")
        return to_clean