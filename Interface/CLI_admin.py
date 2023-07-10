
from os import system, name
from time import sleep
import mysql.connector

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
def chk_admin_pwd(curr,p):
    if(curr ==p):
        return True
    return False
def admin_usr_chk(s):
    try:
        curr = db.cursor()
        string = "select password from administrator where name = %s" %('\''+ s + '\'')
        curr.execute(string)
        ret =  curr.fetchone()
        return (ret[0] if ret != None else False)
    except:
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
    for i in field_names:
        print(i,end=" ")
    print()
    
def isEmpty(query):
    cur.execute(query)
    lt = [len(i) for i in cur]
    if(len(lt)==0):
        return 1
    return 0
def exec_query(s,flag):                             #flag signifies whether the column headers need to be printed
    
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
            print(i[j+1])
            c+=1
        gaps(1)
        print('Total rows returned - ',c)
        print('='*200)
    elif(flag == 2):
        return
    elif (flag == 3):
        return cur.fetchall()
    else:
        for i in cur:
            return i[0]
            

#basic interface- start screen
while(True):
    print("************************************************************************************************************")
    gaps(3)
    shift(30)
    id = input("Name: ")
    shift(30)
    gaps(1)
    exists = admin_usr_chk(id)
    ch = 0
    if(exists):
        shift(30)
        pwd = input("Password: ")
        gaps(3)
        print("************************************************************************************************************")
        sleep(1)
        clear()
        #as Admin
        if(chk_admin_pwd(exists,pwd)):
            #verification check
            gaps(1)
            clear()
            print("Welcome ",id)
            exec_query("GRANT ALL PRIVILEGES ON okina.* TO 'root'@'localhost'", 2)
            gaps(3)
            ch_in=0
            while(ch_in!=5):
                merch = exec_query("select * from adhoc where position = 'merchant'",3)
                deliv = exec_query("select * from adhoc where position = 'delivery_exec'",3)
                assis = exec_query("select * from adhoc where position = 'assister'",3)
                print("Please choose one of the following options:")
                gaps(2)
                print("Press 1 to view all current users")
                # print("Press 2 to add a new user")
                print("Press 2 to view the total revenue generated in past month")
                print("Press 3 to view the best selling product")
                print("Press 4 to get combination of sales according to date")
                print("Press 5 to search any custom query")
                print()
                if(len(merch)):
                    print(len(merch),"Merchant applications enter M to review")
                if(len(deliv)):
                    print(len(deliv),"Delievery Executive applications enter D to review")
                if(len(assis)):
                    print(len(assis),"Technical assister applications enter A to review")
                gaps(1)
                print("Press 6  to exit to main menu")
                gaps(2)
                ch_in = input("Choice: ")
                gaps(2)

                if(ch_in=='1'):
                    query_string = 'select * from user'
                    exec_query(query_string,1)

                elif(ch_in=='2'):
                    query_string = 'select sum(revenue) from sales where date <= \'2023-03-24 00:00:00\' and date >=\'2023-02-24 00:00:00\''
                    ans = exec_query(query_string,0)
                    print("Total revenue generated this past month (in lacs): ",ans)

                elif(ch_in=='3'):
                    query_string = 'select product_ID,size,price,discount,rating from product where product_ID in (select product_ID from sales where profit in (select max(profit) from sales))'
                    exec_query(query_string,1)
                
                elif(ch_in=='4'):
                    query_string = 'select product_ID, year(date), month(date), sum(profit) as net_profit from sales group by product_ID, year(date), month(date) with rollup;'
                    exec_query(query_string,1)

                elif(ch_in=='5'):
                    query_string = input("Enter query: ")
                    f = int(input("Do you wish to print the output for the above query? (1/0): "))
                    exec_query(query_string,f)

                elif(ch_in=='M'):
                    for i in merch:
                        print(i)
                        slash = int(input("Enter 1 for recruiting\n0 for rejecting\n2 to delay\nChoice:"))
                        if(slash == 1):
                            exec_query("insert into merchant(name, contact) values('{}','{}') ".format(i[1], i[2]),2) 
                        if(slash == 1 or slash == 0):  
                            exec_query("delete from adhoc where adhoc_id = {}".format(i[0]),2)
                        db.commit()

                elif(ch_in=='D'):
                    for i in deliv:
                        print(i)
                        sslash = int(input("Enter 1 for recruiting\n0 for rejecting\n2 to delay\nChoice:"))
                        if(slash == 1):
                            exec_query("insert into delivery_exec(name, contact) values('{}','{}') ".format(i[1], i[2]),2)
                        if(slash == 1 or slash == 0):
                            exec_query("delete from adhoc where adhoc_id = {}".format(i[0]),2)
                        db.commit()
                elif(ch_in=='A'):
                    for i in assis:
                        print(i)
                        slash = int(input("Enter 1 for recruiting\n0 for rejecting\n2 to delay\nChoice:"))
                        if(slash == 1):
                            exec_query("insert into assister(name, contact) values('{}','{}') ".format(i[1], i[2]),2)
                        if(slash == 1 or slash == 0):
                            exec_query("delete from adhoc where adhoc_id = {}".format(i[0]),2)
                        db.commit()
                elif(ch_in=='6'):
                    clear()
                    print("Exiting...")
                    gaps(2)
                    exit()

                else:
                    gaps(2)
                    print("Unrecognized input.")
                    print("Exiting...")
                    gaps(2)
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
                    clear()
                break
        else:
            #verification failed
            gaps(2)
            print("Incorret Password.")
            gaps(2)
            print("Press 1 to try again")
            print("Press 2 to exit")
            gaps(2)
            chu = int(input("Choice: "))
            if(chu==1):
                clear()
                ch += 1
                continue
            elif(chu==2):
                clear()
                print("You have chosen to exit")
                gaps(2)
                exit()
            else:
                gaps(2)
                print("Unrecognized input.")
                print("Exiting...")
                gaps(2)
                exit()
    else:
        #verification failed
        gaps(2)
        shift(30)
        print("No user found")
        gaps(2)
        shift(30)
        print("Press 1 to try again")
        shift(30)
        print("Press 2 to exit")
        gaps(2)
        shift(30)
        chu = int(input("Choice: "))
        if(chu==1):
            clear()
            continue
        elif(chu==2):
            clear()
            shift(30)
            print("You have chosen to exit")
            gaps(2)
            exit()
        else:
            gaps(2)
            shift(30)
            print("Unrecognized input.")
            print("Exiting...")
            gaps(2)
            exit()