import yaml, requests, json
from lookerapi import LookerApi
from pprint import pprint

host = 'saleseng'         # looker host name from config file
au = 0                  # set to 1 if hosted in Australia

# -------------------------------------------------


def conn(host, au):
    f = open('config.yml')
    params = yaml.load(f)
    f.close()

    if au == 1:
        my_host = 'https://' + params['hosts'][host]['host'] + '.au.looker.com:19999/api/3.0/'
    else:
        my_host = 'https://' + params['hosts'][host]['host'] + '.looker.com:19999/api/3.0/'

    my_secret = params['hosts'][host]['secret']
    my_token = params['hosts'][host]['token']

    looker = LookerApi(host=my_host, token=my_token, secret=my_secret)
    if looker is None:
        print('Connection to Looker failed')
        exit()

    return looker


def run_inline_query(self,body={}):
    url = '{}{}/run/json'.format(self.host,'queries')
    params = json.dumps(body)
    r = self.session.post(url,data=params)
    if r.status_code == requests.codes.ok:
        return r.json()


looker = conn(host, au)

model = 'fntsypl'               # model name
explore = 'pdt_mapping'         # explore name
table = 'pdt_mapping' + '.'     # table 1 name, add more


fields = [
    table + 'view_sql_mysql'    # fields to query
]

body = {
    'model': model
    , 'view': explore
    , 'fields': fields
    , 'limit': '5'
}

r = looker.run_inline_query(body)

for pdt in r:
    pprint(pdt['pdt_mapping.view_sql_mysql'])   # change to execute mysql cmd to build the view



