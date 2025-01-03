### How to run code 
Simple subscription to coinbase ticker.
```
python3 src/ws_client.py
```

### How to run ab test
You can change count of messages via `total_messages` variable.
There are simple AB tests to compare the time at which the same message is received between 2 connections.
```
python3 src/ws_client_ab_test.py
```

### How to run perf test
You can change count of messages via `total_messages` variable.
There are simple tests for receive latency and aggregate results.

```
python3 src/ws_client_perf_test.py
```

### How to run tests and open allure report
There are 3 simple tests (Check connection, product ID validation, response fields validation).
```
pytest tests/tests_ws_client.py --alluredir=allure-results
allure generate allure-results -o allure-report --clean 
allure open allure-report
```