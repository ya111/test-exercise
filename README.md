### Help is here: 
```
python3 run_app.py
```

### How to run code 
Simple subscription to coinbase ticker.
You can change count of messages via `total_messages`, read more info below.
```
python3 run_app.py ws
```

### How to run ab test
There are simple AB tests to compare the time at which the same message is received between 2 connections.
You can change count of messages via `total_messages`, read more info below.
```
python3 run_app.py ws_ab
```

### How to run perf test
There are simple tests for receive latency and aggregate results.
You can change count of messages via `total_messages`, read more info below.
```
python3 run_app.py ws_perf
```

### How to change the number of messages
```
python3 run_app.py ws --total_messages=10 (default=None)
python3 run_app.py ws_ab --total_messages=15 (default=10)
python3 run_app.py ws_perf --total_messages=15 (default=10)
```

### How to run tests and open allure report
There are 3 simple tests (Check connection, product ID validation, response fields validation).
```
pytest tests/tests_ws_client.py --alluredir=allure-results
allure generate allure-results -o allure-report --clean 
allure open allure-report
```

# Dockerfile
Dockerfile sample
```
docker build -t project_name .
docker run --rm project_name python run_app.py ws_ab --total_messages=50
```