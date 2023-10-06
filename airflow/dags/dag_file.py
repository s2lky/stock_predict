from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta
import psycopg2

# DAG 정의
default_args = {
    'owner': 'your_name',
    'depends_on_past': False,
    'start_date': datetime(2023, 10, 4),
    'retry_delay': timedelta(minutes=1),
}

dag = DAG(
    '06_30_stock_data',
    default_args=default_args,
    schedule_interval='30 6 * * *',  # 매 분마다 실행
    catchup=False,  # 과거 작업을 재실행하지 않음
    tags=['test'],
)

def Collect_Stock_Data(market_name:str):
    default_path = '/opt/airflow/'
    input_file_path = default_path+'dags/tickers/' + market_name + '_ticker.csv'
    output_file_path = default_path+'stock_data/' + market_name + '_data.csv'
    df = pd.read_csv(input_file_path)
    symbols = df['symbol']

    # Initialize an empty DataFrame to store the results
    result = pd.DataFrame()

    # Define the start date and end date
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=1)

    # Loop through the symbols and fetch data
    for symbol in symbols[:5]:
        try:
            data = yf.Ticker(symbol)
            # Fetch stock data for the specified symbol and date range
            symbol_df = data.history(symbol, start=start_date, end=end_date)
            
            # Add the symbol column
            symbol_df.insert(0, 'symbol', symbol)

            # Concatenate the data to the result DataFrame
            result = pd.concat([result, symbol_df])
        
        except Exception as e:
            print(f"An error occurred for symbol {symbol}: {e}")

    
    # Save the result to a CSV file
    result.to_csv(output_file_path)


def pre_processing():
    datas = ['/opt/airflow/stock_data/amex_data.csv', '/opt/airflow/stock_data/nyse_data.csv', '/opt/airflow/stock_data/nasdaq_data.csv']
    for data in datas:
        stock_data = pd.read_csv(data)
        stock_data['Date'] = stock_data['Date'].str.slice(stop=10)
        columns_to_drop = ['Dividends', 'Stock Splits']
        stock_data.drop(columns=columns_to_drop, inplace=True)
        stock_data.to_csv(data, index=False)
        

# PostgreSQL 연결 정보 설정
db_config = {
    "host": "43.201.204.226",
    "database": "test01",
    "user": "manager",
    "password": "P#8sZ2d@7wQ9"
}
def Connect():
    # PostgreSQL에 연결
    conn = psycopg2.connect(**db_config) 
    # 커서 생성
    cursor = conn.cursor()
    return conn, cursor

def Get_Data(df):
    for index, row in df.iterrows():
        return index, (row['Date'], row['symbol'], row['Open'], row['High'], row['Low'], row['Close'], row['Volume'])
    
def Insert_Values(conn, cursor, values):
    # 데이터 삽입 쿼리
    insert_query = "INSERT INTO stock_data (Date, Open, High, Low, Close, Volume) VALUES (%s, %s, %s, %s, %s, %s)"
    # 데이터 삽입
    cursor.execute(insert_query, values)

    # 변경사항 커밋
    conn.commit()

# CSV 파일 경로 설정
def Collect_Job():
    csv_file_path = ['/opt/airflow/stock_data/amex_data.csv', '/opt/airflow/stock_data/nyse_data.csv', '/opt/airflow/stock_data/nasdaq_data.csv']

    conn, cursor = Connect()
    for i in range(3):
        df = pd.read_csv(csv_file_path[i])
        _, values = Get_Data(df=df)
        
        Insert_Values(conn=conn, cursor=cursor, values=values)
            
        print("데이터가 PostgreSQL에 성공적으로 적재되었습니다.")

    cursor.close()
    conn.close()
    # 연결 및 커서 닫기

    
    
task_run_nyse = PythonOperator(
    task_id='collect_nyse',
    python_callable=Collect_Stock_Data,
    op_kwargs={'market_name': 'nyse'},
    dag=dag,
)

task_run_nasdaq = PythonOperator(
    task_id='collect_nasdaq',
    python_callable=Collect_Stock_Data,
    op_kwargs={'market_name': 'nasdaq'},
    dag=dag,
)

task_run_amex = PythonOperator(
    task_id='collect_amex',
    python_callable=Collect_Stock_Data,
    op_kwargs={'market_name': 'amex'},
    dag=dag,
)

task_pre_processing = PythonOperator(
    task_id='pre_processing',
    python_callable=pre_processing,
    dag=dag,
)

task_insert_data = PythonOperator(
    task_id='insert_data',
    python_callable=Collect_Job,
    dag=dag,
)



task_run_nyse >> task_run_nasdaq >> task_run_amex >> task_pre_processing >> task_insert_data

if __name__ == "__main__":
    dag.run()


