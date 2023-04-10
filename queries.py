


make_debt_record = 'INSERT INTO "debt_record" (debtor, creditor, amount, comment, author, datetime, author_id, confirmation) VALUES ({},{},{},"{}","{}","{}",{},{})'
users = "SELECT name FROM user" 
check_user_exist_queries = 'SELECT * FROM user where name="{}"'    
last_row_id = 'SELECT * FROM "{}" ORDER BY id DESC LIMIT 1;'
update_confirmation_status = 'UPDATE debt_record set confirmation = 1 where id = {}'
debt_row_by_id = 'SELECT * from debt_record where id = {}'