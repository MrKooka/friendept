import sqlite3
import queries as q
from collections import namedtuple

User = namedtuple('User', ['id', 'name', 'tgId'])
DebtRow = namedtuple('DebtRow', ['id', 'amount', 'debtor', 'creditor','author', 'datetime', 'comment', 'author_id', 'confirmation'])


        


class DBConnector:
    def __enter__(self):
        self.conn = sqlite3.connect('debptDB.db')
        self.cursor =self.conn.cursor()

        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.conn.close()
    

# class DebtRow(DebtRowNameT):

#     @property
#     def last_row(self):
#         with DBConnector() as db:
#             res = db.cursor.execute(q.last_row_id.format("debt_record")).fetchall()
#             return DebtRow(*res[0])
                

    
def insert_debt(args) -> DebtRow:
    # print(args)
    # print(args['debtor'],args['creditor'],args['amount'],args['comment'],args['author'],args['datetime'], args['author_id'])    
    
    debtor = args['debtor']
    creditor = args['creditor']
    amount = args['amount']
    comment = args['comment']
    author = args['author']
    datetime = args['datetime']
    author_id = args['author_id']
    confirmation = 0
    smt = q.make_debt_record.format(debtor,creditor,amount,comment,author,datetime,author_id,confirmation)
    print(smt)
    with DBConnector() as db:
        db.cursor.execute(smt)
        db.conn.commit()
        last_row_id = db.cursor.lastrowid
    with DBConnector() as db:
        res = db.cursor.execute(q.debt_row_by_id.format(last_row_id)).fetchall()
    return DebtRow(*res[0])


def users():
    with DBConnector() as db:
        cur = db.conn.cursor()
        return db.cursor.execute(q.users).fetchall()
    
def check_user_exist(name: str):
    smt = q.check_user_exist_queries.format(name)
    with DBConnector() as db:
        
        responce = db.cursor.execute(smt).fetchall()

    if responce:
        # [(1, 'alex', 515854171)] - Пример строки из базы
        return User(*responce[0])
    else:
        return False


def approve_confirmation():
    with DBConnector() as db:
        res = db.cursor.execute('UPDATE debt_record SET confirmation=1 WHERE id=(SELECT max(id) FROM debt_record);')
        db.conn.commit()
        return res.fetchall()
            
def set_confirmation_status(row_id):
    with DBConnector() as db:
        db.cursor.execute(q.update_confirmation_status.format(row_id))
        db.conn.commit()