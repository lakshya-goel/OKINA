from os import system, name
from time import sleep
import mysql.connector
from datetime import datetime,timedelta
from random import randint

#connecting to sql server
try:
    db = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    passwd = '24112003',
    database='okina')

except mysql.connector.Error as e:
    print("Error connecting to the database.")
    exit (1)

cur = db.cursor(buffered=True)
query_string = ""

#helper minor functions
def chk_user_cred(s,p):
    try:
        curr = db.cursor()
        string = "select password from user where user_ID = %s" %(s)
        curr.execute(string)
        for i in curr:
            if(i[0]==p):
                return True
        return False
    except Exception as e:
        return False

def clear():
    if name == 'nt':
        _ = system('cls')

def gaps(i):
    for j in range(i):
        print()

def shift(i):
    for j in range(i):
        print(" ",end="")

def print_column_headers():
    field_names = [i[0] for i in cur.description]
    for i in range(len(field_names)-1):
        print(field_names[i],end=" "*(20-len(field_names[i])))
        print('|',end = " ")
    print(field_names[len(field_names)-1])
    print('-'*200)
    

def isEmpty(query):
    cur.execute(query)
    lt = [len(i) for i in cur]
    if(len(lt)==0):
        return 1
    return 0

def exec_query(s,flag=2):                             #flag signifies whether the column headers need to be printed
    
    try:
        cur.execute(s)
    except Exception as e:
        print('No result',e)
        return
    if(flag==1):
        if isEmpty(s):
            print('No result')
            return
        print('='*200)
        print('Query output: ')
        gaps(1)
        print_column_headers()
        l = 0
        cur.execute(s)
        for i in cur:
            l = len(i)
            break
        c=0
        cur.execute(s)
        for i in cur:
            if(c==10):
                gaps(2)
                ans = input("Do you wish to print all records? (y/n): ")
                if(ans=="n"):
                    break
                gaps(1)
            
            #printing each row in output
        
            print(c+1,".",str(i[0])[:20],end=" "*(17-len(str(i[0]))-len(str(c+1))))
            print('|',end=" ")
            for j in range(1,l-1):
                print(str(i[j])[:20],end=" "*(20-len(str(i[j])[:20])))
                print('|',end = " ")
            print(i[l-1])
            c+=1
        gaps(1)
        print('Total rows returned - ',c)
        print('='*200)
    elif flag==0:
        for i in cur:
            return i[0]
    else:
        return

def quantity_check_product(pid,q):
    query_string = 'select stock from product where product_ID = '+pid
    quan = exec_query(query_string,0)
    if(quan>=q and q>=1):
        return 1
    return 0

def searchProduct():
    keywords = [i for i in input("Search for: ").split()]

    #building query
    search = ''
    for i in keywords:
        search+='pt.tag like \'%'+i+'%\' or '
    search=search[:len(search)-3]
    
    ch = input('Set filters (y/n) :')
    gaps(2)
    if(ch.lower() == 'y'):
        query_string = 'select max(price),min(price),max(discount),min(discount),max(rating),min(rating) from product'
        exec_query(query_string,1)
        gaps(2)
        print('Based on the above information, set the following parameters-')
        min_price,max_price = [int(i) for i in input('Price range (min,max): ').split(',')]
        dc = int(input('Minimum discount: '))
        rating = float(input('Minimum rating: '))
        gaps(2)
        search+= ' and price between %s and %s and discount >= %s and rating >= %s'%(min_price,max_price,dc,rating)

    query_string = 'select p.product_ID,p.name,colour,size,composition,price,discount,rating,count(*) as relevance from product as p join product_tags as pt on p.product_ID = pt.product_ID where '+search+' group by product_ID order by relevance desc'
    return query_string

def addProduct(id):
    p_id = (input("Product ID: "))
    query_string = 'select * from product where product_ID = %s'%(p_id)

    if isEmpty(query_string):
        print('No such product exists')
        gaps(2)
        return
    
    try:
        cur.execute(query_string)
        q = int(input("Quantity: "))
        if not quantity_check_product(p_id,q):
            print('Out of stock')
            return
        query_string = 'insert into cart_product values(%s,%s,%s)'%(id,p_id,q)
        cur.execute(query_string)
        db.commit()
        print("Product added successfully.")
        gaps(2)
    except Exception as e:
        print(e)
        gaps(2)


def toAdd(id):
    gaps(2)
    p_id = (input("Product ID: "))
    query_string = 'select * from product where product_ID = %s'%(p_id)

    if isEmpty(query_string):
        print('No such product exists')
        gaps(2)
        return
    
    try:
        cur.execute(query_string)
        print('Where to add the current product ?\n1.Cart\n2.Wishlist\n3.Both\n4.Nowhere')
        wh = int(input('\n-> '))
        gaps(1)
        if(wh==1):
            q = int(input("Quantity: "))
            query_string = 'insert into cart_product values(%s,%s,%s)'%(id,p_id,q)
            cur.execute(query_string)
            print("Product added successfully to cart.")
        elif(wh==2):
            query_string = 'insert into wishlist_product values(%s,%s)'%(id,p_id)
            cur.execute(query_string)
            print("Product added successfully to wishlist.")
        elif(wh==3):
            q = int(input("Quantity: "))
            query_string = 'insert into cart_product values(%s,%s,%s)'%(id,p_id,q)
            cur.execute(query_string)
            query_string = 'insert into wishlist_product values(%s,%s)'%(id,p_id)
            cur.execute(query_string)
            print("Product added successfully to both.")
        db.commit()
        gaps(2)
    except Exception as e:
        print(e)
        gaps(2)
    return

def toAddWishlist(id):
    gaps(2)
    p_id = (input("Product ID: "))
    query_string = 'select * from product where product_ID in (select product_ID from wishlist_product where product_ID = '+p_id+' and user_ID = '+id+')'

    if isEmpty(query_string):
        print('Product not in wishlist')
        gaps(2)
        return
    try:
        cur.execute(query_string)
        q = int(input("Quantity: "))
        query_string = 'insert into cart_product values(%s,%s,%s)'%(id,p_id,q)
        cur.execute(query_string)
        print("Product added successfully.")
        gaps(2)
    except Exception as e:
        print(e)
        gaps(2)

def removeFromWishlist(id):
    gaps(2)
    p_id = (input("Product ID: "))
    query_string = 'select * from product where product_ID in (select product_ID from wishlist_product where product_ID = '+p_id+' and user_ID = '+id+')'

    if isEmpty(query_string):
        print('Product not in wishlist')
        gaps(2)
        return
    try:
        query_string = 'delete from wishlist_product where user_ID = '+id+' and product_ID = '+p_id
        cur.execute(query_string)
        db.commit()
        print("Product removed successfully.")
        gaps(2)
    except Exception as e:
        print(e)
        gaps(2)

def print_order_details(order_id):
    del_date = order_date = ''
    del_id = bill = order_date = del_date = exec_id = exec_rating = 0
    exec_name = exec_ph = ''

    query_string = 'select * from orders where order_id = '+str(order_id)
    cur.execute(query_string)
    for i in cur:
        del_id = i[2]
        order_date = str(i[4])
        bill = i[3]
    query_string = 'select * from delivery_details where delivery_id = '+str(del_id)
    cur.execute(query_string)
    for i in cur:
        exec_id = i[1]
        del_date = str(i[2])
    query_string = 'select * from delivery_exec where exec_id = '+str(exec_id)
    cur.execute(query_string)
    for i in cur:
        exec_name = i[1]
        exec_ph = i[2]
        exec_rating = i[4]

    #printing template
    print('********************************** ORDER DETAILS **********************************')
    gaps(2)
    print('Total order amount: ',bill)
    i,j = order_date.split()
    print('Date of ordering: ',i)
    i,j = del_date.split()
    print('Date of delivery: ',i)
    gaps(1)
    print('Ordered products: ')
    query_string = 'select * from product where product_ID in (select product_ID from ordered_products where order_ID = %s)'%(order_id)
    exec_query(query_string,1)
    gaps(2)
    print('Delivery partner details: ')
    print('Name: ',exec_name)
    print('Contact: ',exec_ph)
    print('Rating: ',exec_rating)
    gaps(1)
    print('***********************************************************************************')

def checkout(id,amt,payment):
    try:
        now = datetime.now()
        current_time = now.strftime("%Y-%m-%d %H:%M:%S")
    
        #applying coupon 
        query_string = 'select max(discount) from offers where validity>=\'%s\' and offers_ID in (select offers_ID from user_offers where user_ID = %s)'%(current_time,id)
        dc = exec_query(query_string,0)
        amt = amt * ( (100-dc)/100 )
        amt = int(amt)
        print('Coupon applied with discount: ',dc)

        #select del_exec
        query_string = 'select exec_ID from delivery_exec where availability = \'available\' and rating = (select max(rating) from delivery_exec where availability = \'available\')'
        exec_id = exec_query(query_string,0)
        query_string = 'update delivery_exec set availability = \'unavailable\' where exec_ID = '+str(exec_id)
        cur.execute(query_string)
        db.commit()

        #create new entry for delivery_details
        query_string = 'SELECT max(delivery_ID)+1 FROM delivery_details'
        del_id = exec_query(query_string,0)

        del_time = now + timedelta(days = randint(1,5))
        delivery_time = del_time.strftime("%Y-%m-%d %H:%M:%S")

        query_string = 'insert into delivery_details values(%s,%s,\'%s\')'%(del_id, exec_id, delivery_time)
        exec_query(query_string)
        db.commit()
        
        #create a new entry for orders table
        query_string = 'SELECT max(order_ID)+1 FROM orders'
        order_id = exec_query(query_string,0)
        order_time = current_time
        query_string = 'insert into orders values(%s,%s,%s,%s,\'%s\')'%(order_id,id, del_id,amt,order_time)
        exec_query(query_string)
        db.commit()

        #add products in cart to ordered_products and remove them from cart_product
        query_string = 'select product_ID,quantity from cart_product where user_ID = '+id
        exec_query(query_string)
        lis = [i for i in cur]
        for i in lis:
            p_id = i[0]
            q = i[1]
            query1 = 'insert into ordered_products values(%s,%s,%s)'%(order_id,p_id,q)
            exec_query(query1)

        query_string = 'delete from cart_product where user_ID ='+id
        exec_query(query_string)
        db.commit()

        #create a new entry for invoice table
        query_string = 'SELECT max(invoice_ID)+1 FROM invoice'
        invoice_id = exec_query(query_string,0)
        query_string = 'insert into invoice values(%s,%s,\'%s\')'%(invoice_id,order_id,payment)
        exec_query(query_string)
        db.commit()

        gaps(2)
        print('Checkout successful.')
        gaps(1)
        print_order_details(order_id)
        return
    
    except Exception as e:
        print('Error while checking out',e)
        return

#basic interface- start screen
ch = 0
while(ch!=2):
    print("************************************************************************************************************")
    gaps(3)
    shift(30)
    print("Press 1 to Login as User")
    shift(30)
    print("Press 2 to Exit")
    shift(30)
    ch = int(input("Choice: "))
    gaps(3)
    print("************************************************************************************************************")
    sleep(1)
    clear()

                   
    #as user
    while(ch==1):
        print("Please enter the following details")
        gaps(2)
        id = input("User ID: ")
        pwd = input("Password: ")
        if(chk_user_cred(id,pwd)):

            #verification check
            ch=3
            clear()
            print("Welcome User")
            gaps(3)
            ch_in=0
            while(ch_in!=7):
                print("Please choose one of the following options:")
                gaps(2)
                print("Press 1 to view all products")
                print("Press 2 to search for products")        #add to cart add to wishlist
                print("Press 3 to view cart")
                print("Press 4 to view wishlist")
                print("Press 5 to add a product to cart")
                print("Press 6 to view offers")
                print("Press 7 to view order history")     #current and past
                print("Press 8 to view queries")
                print("Press 9 to view your account information")
                gaps(1)
                print("Press 10 to exit to main menu")
                gaps(2)
                ch_in = int(input("Choice: "))
                gaps(2)

                #view all products
                if(ch_in==1):
                    query_string = 'select * from see_products'
                    exec_query(query_string,1)

                #search for products
                elif (ch_in ==2):
                    query_string = searchProduct()
                    exec_query(query_string,1)
                    gaps(2)
                    choice = input('Do you wish to select any of these products (y/n): ')
                    while(choice.lower()=='y'):
                        toAdd(id)
                        choice = input('Anymore products (y/n): ')

                #view cart
                elif(ch_in==3):
                    query_string = 'select * from user_products where user_ID = '+id+''
                    exec_query(query_string,1)
                    gaps(2)
                    query_string = 'select cost from cart where user_ID = %s'%(id)
                    ans = exec_query(query_string,0)
                    if(ans < 50): ans = 0
                    print("Total cart value at present = ",ans)
                    if ans!=0:
                        gaps(2)
                        print('Do you wish to: \n1.checkout\n2.edit cart \n3.empty cart\n4.do nothing')
                        choice = int(input('\n-> '))
                        
                        if(choice==1):
                            print('How would you like to pay for your order?\n1.Debit card\n2.Credit card\n3.Bank Transfer (UPI, Netbanking)\n4.E-wallet\n5.Cash on delivery')
                            payment_type = int(input('\n-> '))
                            payment = ''
                            #mapping payment types to int
                            if(payment_type==1):
                                payment = 'debit card'
                            elif(payment_type==2):
                                payment = 'credit card'
                            elif(payment_type==3):
                                payment = 'bank transfer'
                            elif(payment_type==4):
                                payment = 'E-wallet'
                            elif(payment_type==5):
                                payment = 'cash' 
                            else:
                                print('Undefined input')
                                continue
                            checkout(id,ans,payment)

                        elif(choice==2):
                            print('1. Edit quantity for a product\n2.Remove a product from cart')
                            choi = int(input('\n-> '))
                            gaps(2)
                            if(choi==1):
                                p_id = (input("Product ID: "))
                                query_string = 'select * from cart_product where product_ID = %s and user_ID =%s'%(p_id,id)

                                if isEmpty(query_string):
                                    print('No such product in cart')
                                    continue

                                q = int(input("New quantity: "))
                                if(q<0):
                                    q=0
                                if not quantity_check_product(p_id,q):
                                    print("out of stock")
                                    continue

                                query_string = 'delete from cart_product where product_ID = %s and user_ID =%s'%(p_id,id)
                                exec_query(query_string)
                                db.commit()
                                query_string = 'insert into cart_product values(%s,%s,%s)'%(id,p_id,q)
                                exec_query(query_string)
                                db.commit()
                                print("Quantity updated.")

                            elif(choi==2):
                                p_id = (input("Product ID: "))
                                query_string = 'select * from cart_product where product_ID = %s and user_ID =%s'%(p_id,id)

                                if isEmpty(query_string):
                                    print('No such product in cart')
                                    gaps(2)
                                    continue
                                else:
                                    query_string = 'delete from cart_product where product_ID = %s and user_ID =%s'%(p_id,id)
                                    exec_query(query_string)
                                    db.commit()
                                    print('Product removed from cart.')

                        elif(choice==3):
                            query_string = 'delete from cart_product where user_ID =%s'%(id)
                            exec_query(query_string)
                            db.commit()
                            print("Cart emptied.")
                            

                #view wishlist
                elif(ch_in==4):
                    query_string = 'select * from product where product_ID in (select product_ID from wishlist_product where user_ID = '+id+')'
                    exec_query(query_string,1)
                    if not isEmpty(query_string):
                        exec_query(query_string)
                        l = [i for i in cur]
                        #add to cart
                        gaps(2)
                        print('Do you wish to: \n1.add any product to cart\n2.add all of these products to cart \n3.remove some products from wishlist\n4.do nothing')
                        choice = int(input('\n-> '))
                        if(choice==1):
                            choi = 'y'
                            while(choi.lower()=='y'):
                                toAddWishlist(id)
                                choi = input('Anymore products (y/n): ')
                                gaps(1)

                        elif(choice==2):
                            for i in l:
                                cur.execute('insert into cart_product values(%s,%s,%s)'%(id,i[0],1))
                            db.commit()
                            print('All products from wishlist added to cart.')
                        elif(choice==3):
                            choi = 'y'
                            while(choi.lower()=='y'):
                                removeFromWishlist(id)
                                choi = input('Anymore products (y/n): ')
                                gaps(1)

                        
                    #clear wishlist

                #add product to cart
                elif(ch_in==5):
                    addProduct(id)
                        
                #view offers
                elif(ch_in==6):
                    query_string = 'select * from offers where offers_ID in (select offers_ID from user_offers where user_ID = %s)'%(id) #try with user no.69, it has 4 offers.
                    exec_query(query_string,1)

                #view order history
                elif(ch_in==7):
                    print('1.View active orders\n2.View past orders')
                    choice = int(input('\n-> '))
                    now = datetime.now()
                    current_time = now.strftime("%Y-%m-%d %H:%M:%S")
                    if(choice!=1 and choice!=2):
                        print('Undefined input')
                        continue
                    elif(choice==1):
                        query_string = 'select * from orders where delivery_ID in (select delivery_ID from delivery_details as d where d.datetime > \'%s\') and user_ID = %s'%(current_time,id)            
                    elif(choice==2):
                        query_string = 'select * from orders where delivery_ID in (select delivery_ID from delivery_details as d where d.datetime <= \'%s\') and user_ID = %s'%(current_time,id) 
                    
                    exec_query(query_string,1)
                    if not isEmpty(query_string):
                        choi = input('View details for an order? (y/n): ')
                        if(choi.lower()=='y'):
                            order_id = int(input('Enter order id: '))
                            query_string = 'select * from orders where user_ID =%s'%(id)

                            if isEmpty(query_string):
                                print('Wrong order id.')
                                continue

                            print_order_details(order_id)
                            gaps(2)
                            chhoi = input('Raise a query regarding this order?(y/n): ')
                            if(chhoi=='y'):
                                query_string = 'insert into assistance (order_ID, status) values(%s,\'%s\')'%(order_id,'pending')
                                exec_query(query_string)
                                db.commit()
                                print('Query raised successfully.')
                            

                #assistance
                elif(ch_in==8):
                    print('1.View resolved queries\n2.View unresolved queries')
                    choice = int(input('\n-> '))
                   
                    if(choice==1):
                        query_string = 'select * from assistance where status = \'resolved\' and user_ID = '+id
                        exec_query(query_string,1)
                                
                    elif(choice==2):
                        query_string = 'select * from assistance where status = \'pending\' and user_ID = '+id
                        exec_query(query_string,1)
                    
                    else:
                        print('Undefined input')
                        continue

                elif(ch_in==9):
                    print("Your current details - ")
                    gaps(2)
                    query_string = 'select username from user where user_ID = '+str(id)
                    username = exec_query(query_string,0)
                    print('Current username: ',username)
                    query_string = 'select contact as Currently_saved_contacts from user_contact where user_ID = '+str(id)
                    exec_query(query_string,1)
                    gaps(1)
                    query_string = 'select address as Currently_saved_addresses from user_address where user_ID = '+str(id)
                    exec_query(query_string,1)

                    print('Press 1 to change username.\nPress 2 to add/delete a contact\nPress 3 to add/delete an address\nPress 4 to do nothing')
                    choice = int(input('->'))

                    if(choice==1):
                        uname = input('New username: ')
                        query_string='update user set username = \'%s\' where user_ID = %s'%(uname,id)
                        exec_query(query_string)
                        db.commit()
                        print('\nUsername updated successfully.')

                    elif(choice==2):
                        print('Press 1 to add contact.\nPress 2 to delete a contact')
                        chhoi = int(input('->'))
                        if(chhoi==1):
                            cont = input('New contact (###-###-####): ')
                            query_string = 'insert into user_contact values (%s,\'%s\')'%(id,cont)
                            exec_query(query_string)
                            db.commit()
                        elif(chhoi==2):
                            cont = input('Contact number to delete: ')
                            query_string = 'delete from user_contact where user_ID = %s and contact = \'%s\''%(id,cont)
                            exec_query(query_string)
                            db.commit()
                    elif(choice==3):
                        print('Press 1 to add address.\nPress 2 to delete address')
                        chhoi = int(input('->'))
                        if(chhoi==1):
                            cont = input('New address (max 250 chars): ')
                            query_string = 'insert into user_address values (%s,\'%s\')'%(id,cont)
                            exec_query(query_string)
                            db.commit()
                        elif(chhoi==2):
                            cont = input('Enter address to delete: ')
                            query_string = 'delete from user_address where user_ID = '+str(id)+' and address like \'%'+str(cont)+'%\''
                            exec_query(query_string)
                            db.commit()
                        
                elif(ch_in==10):
                    clear()
                    print("Exiting...")
                    ch_in=7
                    ch=3
                    continue

                else:
                    gaps(2)
                    print("Unrecognized input.")
                    print("Exiting...")
                    exit()

                #continue dialogs
                gaps(2)
                print('Enter 1 to continue with another query')
                print('Enter 2 to exit to main menu')
                gaps(1)
                ch_in=int(input("Choice: "))
                if(ch_in==1):
                    clear()
                    continue
                else:
                    ch_in=7
                    ch=3
                    clear()
                    break

        else:
            #verification failed
            gaps(2)
            print("The submitted details don't match our database.")
            gaps(2)
            print("Press 1 to try again")
            print("Press 2 to exit to main menu")
            gaps(2)
            ch = int(input("Choice: "))
            if(ch==1):
                clear()
                continue
            elif(ch==2):
                clear()
                print("You have chosen to exit to main menu")
                break
            else:
                gaps(2)
                print("Unrecognized input.")
                print("Exiting...")
                exit()
        continue
        
    if(ch==2):
        clear()
        print("You have chosen to exit")
        exit()

    elif(ch==3):
        clear()
        continue

    else:
        clear()
        print("Unrecognized input.")
        print("Try again.")
        gaps(2)
                