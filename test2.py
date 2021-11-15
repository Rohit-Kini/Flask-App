import requests
BASE = "http://127.0.0.1:5000/"

policy = [{"customer_income": 500, "customer_debt":500, "payment_remarks_12m":0, "payment_remarks":1, "customer_age":20},
          {"customer_income": 1000, "customer_debt":500, "payment_remarks_12m":0, "payment_remarks":2, "customer_age":20},
          {"customer_income": 499, "customer_debt":100, "payment_remarks_12m":0, "payment_remarks":1, "customer_age":17},
          {"customer_income": 1500, "customer_debt":500, "payment_remarks_12m":1, "payment_remarks":1, "customer_age":35},
          {"customer_income": 800, "customer_debt":350, "payment_remarks_12m":2, "payment_remarks":0, "customer_age":48}]


for i in range(len(policy)):
    response = requests.post(BASE+"checkpolicy", json=policy[i])
    print(response.json())

print("Test Case Finished")