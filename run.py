#!/usr/bin/env python

import os
import sys
from   time import sleep

from lib.budget import Budget
from lib.notion import Notion

class Configuration:

    def __init__(self):

        ''' Load enviroment variables from env.sh '''
        self.notion_api_key   = os.environ.get( 'NOTION_API_KEY',   None )
        self.notion_budget_db = os.environ.get( 'NOTION_BUDGET_DB', None )
        self.notion_url       = os.environ.get( 'NOTION_URL',       None )
        self.mysql_host       = os.environ.get( 'MYSQL_HOST',       None )
        self.mysql_db         = os.environ.get( 'MYSQL_DB',         None )
        self.mysql_port       = os.environ.get( 'MYSQL_PORT'  ,     None )
        self.mysql_user       = os.environ.get( 'MYSQL_USER',       None )
        self.mysql_pass       = os.environ.get( 'MYSQL_PASS',       None )

        if self.notion_api_key == None: 
            print('Error: NOTION_API_KEY undefined!')
            sys.exit(1)
        elif self.notion_budget_db == None:
            print('Error: NOTION_BUDGET_DB undefined!')
            sys.exit(1)
        elif self.notion_url == None:
            print('Error: NOTION_URL undefined!')
            sys.exit(1)
        elif self.mysql_host == None:
            print('Error: MYSQL_HOST undefined!')
            sys.exit(1)
        elif self.mysql_db == None:
            print('Error: MYSQL_DB undefined!')
            sys.exit(1)
        elif self.mysql_port == None:
            print('Error: MYSQL_PORT undefined!')
            sys.exit(1)
        elif self.mysql_user == None:
            print('Error: MYSQL_USER undefined!')
            sys.exit(1)
        elif self.mysql_pass == None:
            print('Error: MYSQL_PASS undefined!')
            sys.exit(1)
     
class Actions:

    def __init__(self):
        pass
        
    def update_budget_database(self):
        
        '''
            
            Here we create two objects:
                - notion_ids  : a list of ids that identify the Notion budget entries
                - budget_data : a list of budget entries

        '''

        notion      = Notion(Configuration())
        notion_data = notion.get_budget_database_data()
        notion_ids  = []
        budget_data = []

        for data in notion_data:
            for item in data:
                notion_ids.append(item['id'])
                budget_data.append(item)
        
        data_budget_parsed = notion.parse_budget_data(budget_data)

        '''
            
            Here we'll send data_budget_parsed to the method 
            that will parse and input all data into database

        '''

        budget = Budget(Configuration())
        budget.sync(data_budget_parsed)

        ''' 
            Finally we delete all ids that is not in the 'notion_ids
        '''

        budget.delete(notion_ids)

if __name__ == '__main__':
    while True:
        actions = Actions()
        actions.update_budget_database()
        sleep(10)