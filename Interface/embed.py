import mysql.connector
db = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    passwd = '24112003',
    auth_plugin='mysql_native_password',
    database='okina'
)

cur = db.cursor()
user = int(input("Enter user ID: "))

cur.execute("select product_ID from cart_product where user_id = "+str(user)) #query 1
lst = []
print("The following item contained in cart")
for i in cur:
    lst.append(i[0])
print("price | quantity")
for i in lst:
    cur.execute("select name, price from product where product_ID = "+str(i)) #query 2
    for j in cur:
        print(j[0],' | ', j[1])