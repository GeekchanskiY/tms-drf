from raw_celety_srv import add as send_email

for i in range(100):
    print(send_email(i, i))
