import datetime
import time
import psycopg2

import requests
import json
import pandas as pd
import numpy as np

from airflow import DAG
from airflow.providers.http.operators.http import SimpleHttpOperator
from airflow.operators.python import PythonOperator
from airflow.hooks.base import BaseHook
from airflow.models.xcom import XCom

###API settings###
#set api connection from basehook
api_conn = BaseHook.get_connection('create_files_api')
#d5dg1j9kt695d30blp03.apigw.yandexcloud.net
api_endpoint = api_conn.host
#5f55e6c0-e9e5-4a9c-b313-63c01fc31460
api_token = api_conn.password

#set user constants for api
nickname = "senigov"
cohort = "XX"

headers = {
    "X-API-KEY": api_conn.password,
    "X-Nickname": nickname,
    "X-Cohort": cohort
}


###POSTGRESQL settings###
#set postgresql connectionfrom basehook
psql_conn = BaseHook.get_connection('postgresql_de')

##init test connection
conn = psycopg2.connect(f"dbname='de' port='{psql_conn.port}' user='{psql_conn.login}' host='{psql_conn.host}' password='{psql_conn.password}'")
cur = conn.cursor()
cur.close()
conn.close()





#1. запрашиваем выгрузку файликов
#получаем в итоге стринг task_id идентификатор задачи выгрузки
#где то через 60 секунд должен сформироваться по другому пути ссылка на доступ к выгруженным файлам
def create_files_request(ti, api_endpoint , headers):
    method_url = '/generate_report'
    r = requests.post('https://'+api_endpoint + method_url, headers=headers)
    response_dict = json.loads(r.content)
    ti.xcom_push(key='task_id', value=response_dict['task_id'])
    print(f"task_id is {response_dict['task_id']}")
    return response_dict['task_id']



#2. проверяем готовность файлов в success
#на выход получаем стринг идентификатор готового репорта который является ссылкой до файлов которые можем скачивать
def check_report(ti, api_endpoint , headers):
    task_ids = ti.xcom_pull(key='task_id', task_ids=['create_files_request'])
    task_id = task_ids[0]
    
    method_url = '/get_report'
    payload = {'task_id': task_id}

    #отчет выгружается 60 секунд минимум - самое простое в слип на 70 секунд уводим - делаем 4 итерации - если нет то пусть валится в ошибку
    #значит с выгрузкой что-то не так по api и надо идти разбираться с генерацией данных - и в жизни такая же фигня бывает
    for i in range(4):
        time.sleep(70)
        r = requests.get('https://' + api_endpoint + method_url, params=payload, headers=headers)
        response_dict = json.loads(r.content)
        print(i, response_dict['status'])
        if response_dict['status'] == 'SUCCESS':
            report_id = response_dict['data']['report_id']
            break
    
    #тут соответствуенно если report_id не объявлен то есть не было сукксесса то в ошибку упадет и инженер идет разбираться почему
    #можно сделать красивее но время
    ti.xcom_push(key='report_id', value=report_id)
    print(f"report_id is {report_id}")
    return report_id




#3. загружаем 3 файлика в таблички (таблички stage)
def upload_from_s3_to_pg(ti,nickname,cohort):
    report_ids = ti.xcom_pull(key='task_id', task_ids=['create_files_request'])
    report_id = report_ids[0]

    storage_url = 'https://storage.yandexcloud.net/s3-sprint3/cohort_{COHORT_NUMBER}/{NICKNAME}/{REPORT_ID}/{FILE_NAME}'

    personal_storage_url = storage_url.replace("{COHORT_NUMBER}", cohort)
    personal_storage_url = personal_storage_url.replace("{NICKNAME}", nickname)
    personal_storage_url = personal_storage_url.replace("{REPORT_ID}", report_id)


    #insert to database
    psql_conn = BaseHook.get_connection('postgresql_de')
    conn = psycopg2.connect(f"dbname='de' port='{psql_conn.port}' user='{psql_conn.login}' host='{psql_conn.host}' password='{psql_conn.password}'")
    cur = conn.cursor()

    #get custom_research
    df_customer_research = pd.read_csv(personal_storage_url.replace("{FILE_NAME}", "customer_research.csv") )
    insert_cr = "insert into stage.customer_research (date_id,category_id,geo_id,sales_qty,sales_amt) VALUES {cr_val};"
    i = 0
    step = int(df_customer_research.shape[0] / 100)
    while i <= df_customer_research.shape[0]:
        print('df_customer_research' , i, end='\r')
        
        cr_val =  str([tuple(x) for x in df_customer_research.loc[i:i + step].to_numpy()])[1:-1]
        cur.execute(insert_cr.replace('{cr_val}',cr_val))
        conn.commit()
        
        i += step+1

    #get order log
    df_order_log = pd.read_csv(personal_storage_url.replace("{FILE_NAME}", "user_orders_log.csv") )
    insert_uol = "insert into stage.user_order_log (date_time, city_id, city_name, customer_id, first_name, last_name, item_id, item_name, quantity, payment_amount) VALUES {uol_val};"
    i = 0
    step = int(df_order_log.shape[0] / 100)
    while i <= df_order_log.shape[0]:
        print('df_order_log',i, end='\r')
        
        uol_val =  str([tuple(x) for x in df_order_log.drop(columns = ['id'] , axis = 1).loc[i:i + step].to_numpy()])[1:-1]
        cur.execute(insert_uol.replace('{uol_val}',uol_val))
        conn.commit()
        
        
        i += step+1

    #get activity log
    df_activity_log = pd.read_csv(personal_storage_url.replace("{FILE_NAME}", "user_activity_log.csv") )
    insert_ual = "insert into stage.user_activity_log (date_time, action_id, customer_id, quantity) VALUES {ual_val};"
    i = 0
    step = int(df_activity_log.shape[0] / 100)
    while i <= df_activity_log.shape[0]:
        print('df_activity_log',i, end='\r')
        
        ual_val =  str([tuple(x) for x in df_activity_log.drop(columns = ['id'] , axis = 1).loc[i:i + step].to_numpy()])[1:-1]
        cur.execute(insert_ual.replace('{ual_val}',ual_val))
        conn.commit()
        
        
        i += step+1


    cur.close()
    conn.close()

    #понятно что можно обернуть в функцию но для времени описал 3 разными запросами просто для экономии
    return 200


#3. обновляем таблички d по загруженными в stage



#4. апдейт витринок (таблички f)




#Объявляем даг
dag = DAG(
    dag_id='4_export_data_api_s3_pg_update',
    schedule_interval='0 0 * * *',
    start_date=datetime.datetime(2021, 1, 1),
    catchup=False,
    #dagrun_timeout=datetime.timedelta(minutes=60)
)




t_file_request = PythonOperator(task_id='create_files_request',
                                        python_callable=create_files_request,
                                        op_kwargs={'api_endpoint':api_endpoint,
                                                    'headers': headers
                                                    },
                                        dag=dag)

t_check_report = PythonOperator(task_id='check_ready_report',
                                        python_callable=check_report,
                                        op_kwargs={'api_endpoint':api_endpoint,
                                                    'headers': headers
                                                    },
                                        dag=dag)

t_upload_from_s3_to_pg = PythonOperator(task_id='upload_from_s3_to_pg',
                                        python_callable=check_report,
                                        op_kwargs={'nickname':nickname,
                                                    'cohort': cohort
                                                    },
                                        dag=dag)

t_file_request >> t_check_report >> t_upload_from_s3_to_pg