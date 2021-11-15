import requests
BASE = "http://127.0.0.1:5000/"


policy = [{"customer_income": 1000, "customer_debt":500, "payment_remarks_12m":0, "payment_remarks":1, "customer_age":20},
          {"customer_income": 500, "customer_debt":500, "payment_remarks_12m":0, "payment_remarks":1, "customer_age":20},
          {"customer_income": 2000, "customer_debt":500, "payment_remarks_12m":0, "payment_remarks":1, "customer_age":20},
          {"customer_income": 450, "customer_debt":500, "payment_remarks_12m":0, "payment_remarks":1, "customer_age":20},
          {"customer_income": 1500, "customer_debt":500, "payment_remarks_12m":0, "payment_remarks":1, "customer_age":20},
          {"customer_income": 300, "customer_debt":500, "payment_remarks_12m":0, "payment_remarks":1, "customer_age":20}]

"""
# 1. PUT Method - Adding policies to the database
"""
print("1. PUT Method - Adding {} policies to the database".format(len(policy)))
for i in range(len(policy)):
    response = requests.put(BASE+"policy/" + str(i), policy[i])
    print(response.json())

input("Press Enter to proceed!")

"""
# 2. GET Method - Retrieving the policy from the database
"""
print("2. Get Method - Retrieving the policy from the database")
response = requests.get(BASE+ "policy/5")
print(response.json())

input("Press Enter to proceed!")

"""
# 3. PATCH Method - Update the data from the existing database
"""
print("3. Patch Method - Updating the data from the existing database")
response = requests.patch(BASE+"policy/4", {"customer_age":35})
print(response.json())

input("Press Enter to proceed!")

"""
# 4. DELETE Method - Delete a policy from the database
"""
response = requests.get(BASE+ "policy/3")
print(response.json())

print("Deleting Policy #3......")
response = requests.delete(BASE+"policy/3")

input("Press Enter to proceed!")

"""
# 5. POST Method - Check if exisiting policy is ACCEPT or REJECT
"""
print("5. Checking the policy whether it should be accepted for rejected")
response = requests.post(BASE+"policy/1")
print(response.json())

print("Test Cases Finished")
