import sys
import json
import requests
from datetime import datetime

class Notion:
    
    def __init__(self, config):
        self.config = config
        self.headers = {
            'Authorization'  : f'Bearer {self.config.notion_api_key}',
            'Notion-Version' : '2022-06-28'
        }
    
    def parse_budget_data(self, data):
        
        try:
            items   = []

            for result in data:
                
                __notion_id = result['id']
                __name      = result['properties']['name']['title'][0]['plain_text']
                __category  = result['properties']['category']['select']['name']
                __method    = result['properties']['method']['select']['name']
                __type      = result['properties']['type']['select']['name']
                __value     = result['properties']['value']['number']
                __date      = result['properties']['date']['date']['start']

                items.append({
                    'notion_id' : __notion_id,
                    'name'      : __name,
                    'category'  : __category,
                    'method'    : __method,
                    'type'      : __type,
                    'value'     : __value,
                    'date'      : __date
                })

            return items
        except Exception as err:
            print(f'Error: {err}')
            pass
    
    def get_budget_database_data(self, **kwargs):

        try:
        
            has_more     = True
            start_cursor = None

            while has_more:    
            
                if start_cursor == None:
                    json_data = {}
                else:         
                    json_data = {
                        'start_cursor' : start_cursor
                    }
                
                headers = {
                    'Authorization'  : f'Bearer {self.config.notion_api_key}',
                    'Notion-Version' : '2022-06-28',
                    'Content-Type'   : 'application/json'
                }

                url = f'{self.config.notion_url}/v1/databases/{self.config.notion_budget_db}/query'
                req = requests.post(
                    url, 
                    json=json_data, 
                    headers=headers, 
                    timeout=10)

                data = json.loads(req.text)
                
                yield data['results']
                
                if data.get('has_more') == True:
                    start_cursor = data.get('next_cursor')
                else:
                    break

        except Exception as err:
            print(f'Error: {str(err)}')
            pass

