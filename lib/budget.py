import mysql.connector

class Budget:
    
    def __init__(self, config):
        
        self.config = config
        self.conn   = mysql.connector.connect(
            host     = self.config.mysql_host,
            user     = self.config.mysql_user,
            password = self.config.mysql_pass,
            database = self.config.mysql_db,
            port     = self.config.mysql_port
        )
        self.conn.autocommit = False
    
    def get_budget_data(self):
         
        cursor  = self.conn.cursor()
        query   = 'select * from budget'
        cursor.execute(query)
        data    = cursor.fetchall()
        columns = list(cursor.column_names)
        
        budget_data = []

        for line in data:
            item = dict(zip(columns, list(line)))
            budget_data.append(item)

        return budget_data

    def insert(self, data):
        
        cursor = self.conn.cursor()
        query = 'insert into budget (notion_id, \
              name,category,method,_type,value,date) \
              values ("{}","{}","{}","{}","{}","{}","{}")'.format(
                data.get('notion_id'), 
                data.get('name'), 
                data.get('category'), 
                data.get('method'), 
                data.get('type'), 
                data.get('value'), 
                data.get('date')
              )
        cursor.execute(query)
        cursor.close()

    def update(self, data):
        
        cursor = self.conn.cursor()
        query = 'update budget set \
                    name     = "{}",\
                    category = "{}",\
                    method   = "{}",\
                    _type    = "{}",\
                    value    = "{}",\
                    date     = "{}" where notion_id="{}"'.format(
                        data.get('name'), 
                        data.get('category'), 
                        data.get('method'), 
                        data.get('type'), 
                        data.get('value'), 
                        data.get('date'),
                        data.get('notion_id')
                    )
        cursor.execute(query)
        cursor.close()

    def delete(self, valid_ids):
        
        # get ids to compare
        query  = 'select notion_id from budget'
        cursor = self.conn.cursor()
        cursor.execute(query)
        ids_to_compare = [ x[0] for x in cursor.fetchall() ]
        ids_to_remove  = [ x for x in ids_to_compare if x not in valid_ids]

        if len(ids_to_remove) > 0:
            if len(ids_to_remove) == 1:
                notion_id = ids_to_remove[0]
                query = 'delete from budget where notion_id = "{}"'.format(notion_id)    
            else:
                query = 'delete from budget where notion_id in {}'.format(tuple(ids_to_remove))
            cursor.execute(query)
            cursor.close()
            self.conn.commit()

    def sync(self, data):
        try:
            current_data = self.get_budget_data()
            new_data     = data

            current_data_ids = [ x['notion_id'] for x in current_data ]
            
            for item in new_data:
                if item['notion_id'] not in current_data_ids:
                    self.insert(item)
                elif item['notion_id'] in current_data_ids:
                    self.update(item)
            
            self.conn.commit()

        except Exception as err:
            print(f'erro {str(err)}')
            pass