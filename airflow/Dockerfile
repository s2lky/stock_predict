FROM apache/airflow:2.7.1
COPY requirements.txt /requirements.txt
RUN pip install --user --upgrade pip
RUN pip install -r /requirements.txt
RUN mkdir -p /opt/airflow/stock_data
COPY ./dags/tickers/ ./dags/tickers
