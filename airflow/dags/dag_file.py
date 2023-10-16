from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import pandas as pd
from datetime import datetime, timedelta
from sqlalchemy import create_engine
import yfinance as yf

# DAG 정의
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 10, 4),
    'retry_delay': timedelta(minutes=30),
}

dag = DAG(
    'yf_dag',
    default_args=default_args,
    schedule_interval='00 10 * * *',  # 매 분마다 실행
    catchup=False,  # 과거 작업을 재실행하지 않음
    tags=['maybe'],
)

def Collect_Stock_Data(market_name:str):
    default_path = '/opt/airflow/'
    input_file_path = default_path+'dags/tickers/' + market_name + '_ticker.csv'
    output_file_path = default_path+'stock_data/' + market_name + '_data.csv'
    df = pd.read_csv(input_file_path)
    symbols = df['code']

    # Initialize an empty DataFrame to store the results
    result = pd.DataFrame()

    # Define the start date and end date
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=1)

    # Loop through the symbols and fetch data
    for symbol in symbols:
        try:
            # Fetch stock data for the specified symbol and date range
            symbol_df = yf.download(symbol, start=start_date, end=end_date)
            
            # Add the symbol column
            symbol_df.insert(0, 'company_code', symbol)

            # Concatenate the data to the result DataFrame
            result = pd.concat([result, symbol_df])
        
        except Exception as e:
            print(f"An error occurred for symbol {symbol}: {e}")

    
    # Save the result to a CSV file
    result.to_csv(output_file_path)


def pre_processing():
    datas = ['/opt/airflow/stock_data/amex_data.csv', '/opt/airflow/stock_data/nyse_data.csv', '/opt/airflow/stock_data/nasdaq_data.csv']

    for i in range(len(datas)):
        stock_data = pd.read_csv(datas[i])
        # stock_data = stock_data.rename(columns={'Unnamed: 0': 'Date'})
        stock_data['Date'] = stock_data['Date'].str.slice(stop=10)
        stock_data.columns = stock_data.columns.str.lower()
        stock_data.drop(columns='adj close', inplace=True)
        stock_data.dropna(axis=0, inplace=True)
        stock_data['volume'] = stock_data['volume'].astype(int)
        stock_data.to_csv(datas[i], index=False)
        

# PostgreSQL 연결 정보 설정
db_connection = "postgresql://manager:tPZm7M7gAC8UKeNAf3yf@43.201.204.226:5432/test01"


def Insert_Values(df, table_name, engine):
    # DataFrame을 PostgreSQL 테이블에 적재
    df.to_sql(table_name, engine, if_exists='append', index=False)


# CSV 파일 경로 설정
def Collect_Job():
    engine = create_engine(db_connection)
    markets = ['amex', 'nyse', 'nasdaq']

    for market in markets:
        csv_file_path = f'/opt/airflow/stock_data/{market}_data.csv'
        df = pd.read_csv(csv_file_path)
        # 공휴일, 주말 제외
        if len(df) == 0:
            break
        else:
            Insert_Values(df=df, table_name=market, engine=engine)
                
            print("데이터가 PostgreSQL에 성공적으로 적재되었습니다.")
    # 연결 및 커서 닫기
    engine.dispose()

    
with dag:    
    task_run_nyse = PythonOperator(
        task_id='collect_nyse',
        python_callable=Collect_Stock_Data,
        op_kwargs={'market_name': 'nyse'},
    )

    task_run_nasdaq = PythonOperator(
        task_id='collect_nasdaq',
        python_callable=Collect_Stock_Data,
        op_kwargs={'market_name': 'nasdaq'},
    )

    task_run_amex = PythonOperator(
        task_id='collect_amex',
        python_callable=Collect_Stock_Data,
        op_kwargs={'market_name': 'amex'},
    )

    task_pre_processing = PythonOperator(
        task_id='pre_processing',
        python_callable=pre_processing,
    )
    
    task_insert_data = PythonOperator(
        task_id='insert_data',
        python_callable=Collect_Job,
    )



task_run_nyse >> task_run_nasdaq >> task_run_amex >> task_pre_processing >> task_insert_data

if __name__ == "__main__":
    dag.run()



