import mysql.connector as lakshmi
from datetime import date

con=lakshmi.connect(user='root',host='localhost',password='mvl123',database='Restorent')
cur=con.cursor()
while True:
    print('1.user login')
    print('2.Admin login')
    print('3.exit')
    ch=input('choose one option:')
    if ch=='1':
         name = input("Enter name: ")
         mobile = input("Enter mobile: ")
         password = input("Set password: ")
         cur.execute("INSERT INTO users (name, mobile, password) VALUES (%s, %s, %s)", (name, mobile, password))
         con.commit()
         print("Welcome to Vcube Hotel")
         while True:
             print('1.view menu')
             print('2.Add item to cart')
             print('3.Modify cart')
             print('4.Bill')
             ch=input('enter one option')
             if ch=='1':
                 cur.execute("SELECT * FROM menu")
                 print("MENU:")
                 for r in cur.fetchall():
                  print(f"{r[0]}. {r[1]} | {r[2]} | ₹{r[3]}")
                  
             elif ch=='2':
                 item_id = int(input("Enter item ID to add: "))
                 quantity = int(input("Enter quantity: "))
                 cur.execute('''SELECT price FROM menu WHERE item_id=%s''', (item_id,))
                 result = cur.fetchone()
                 print(result)
                 if result:
                    price = result[0]
                    total = price * quantity
                    user_id=input('enter the user_id:')
                    cur.execute("INSERT INTO orders (user_id, item_id, quantity, order_date, total_price) VALUES (%s, %s, %s, %s, %s)",
                                (user_id, item_id, quantity, date.today(), total))
                    con.commit()
                    print("Item added to cart.")
                 else:
                    print("Invalid item ID.")
             elif ch=='3':
                order_id = int(input("Enter Order ID to modify: "))
                user_id = int(input("Enter new quantity: "))
                cur.execute("SELECT item_id FROM orders WHERE order_id=%s AND user_id=%s", (order_id, user_id))
                row = cur.fetchone()
                if row:
                    item_id = row[0]
                    cur.execute("SELECT price FROM menu WHERE item_id=%s", (item_id,))
                    price = cur.fetchone()[0]
                    new_total = price * new_qty
                    cur.execute("UPDATE orders SET quantity=%s, total_price=%s WHERE order_id=%s", (new_qty, new_total, order_id))
                    con.commit()
                    print("Cart updated.")
                else:
                    print("Order not found for this user.")
             elif ch=='4':
                 cur.execute("""SELECT m.item_name, o.quantity, m.price, o.total_price
                       FROM orders o JOIN menu m ON o.item_id = m.item_id
                               WHERE o.user_id = %s""", (user_id,))
                 rows = cur.fetchall()
                 total = 0
                 print("YOUR BILL")
                 print("-" * 40)
                 for name, qty, price, subtotal in rows:
                    print(f"{name} x{qty} @ ₹{price} = ₹{subtotal}")
                    total += subtotal
                 print("-" * 40)
                 print(f"Total Bill: ₹{total}")
                 print("-" * 40)
             elif ch=='5':
                print("👋Thank you for visiting Vcube Hotel!")
                break
             cur.close()
             con.close()
                                  
               
    elif ch == "2":
        name = input("Enter name: ")
        password = input("Enter password: ")
        #cur.execute("SELECT user_id FROM users WHERE name=%s AND password=%s", (name, password))
        #row = cur.fetchone()
        #if row:
            #user_id = row[0]
            #print("Login successful.")
            #input("Press Enter to continue...")
        if name=='lakshmi' and password=='1234':
            while True:
                print("1. Add menu ")
                print("2. View Menu")
                print('3.Delete menu')
                print('4.modify menu')
                print('5.View all orders')
                print('6.day wise profit')
                op=input('enter one option:')
                if op=='1':
                    item_name = input("Item Name: ")
                    category = input("Category: ")
                    price = float(input("Price: "))
                    cur.execute("INSERT INTO menu (item_name, category, price) VALUES (%s, %s, %s)", (item_name, category, price))
                    con.commit()
                    print("Item added.")
                elif op=='2':
                     cur.execute("SELECT * FROM menu")
                     print("MENU:")
                     for r in cur.fetchall():
                        print(f"{r[0]}. {r[1]} | {r[2]} | ₹{r[3]}")
                elif op=='3':
                     item_id = input("Enter item ID to delete: ")
                     cur.execute("DELETE FROM menu WHERE item_id=%s", (item_id,))
                     con.commit()
                     print("Item deleted.")
                elif op=='4':
                     item_id = input("Enter item ID to modify: ")
                     new_price = float(input("Enter new price: "))
                     cur.execute("UPDATE menu SET price=%s WHERE item_id=%s", (new_price, item_id))
                     con.commit()
                elif op=='5':
                     cur.execute("""SELECT o.order_id, u.name, m.item_name, o.quantity, o.total_price, o.order_date
                                   FROM orders o
                                   JOIN users u ON o.user_id = u.user_id
                                   JOIN menu m ON o.item_id = m.item_id""")
                     print("\n--- All Orders ---")
                     for r in cur.fetchall():
                        print(f"OrderID: {r[0]}, User: {r[1]}, Item: {r[2]}, Qty: {r[3]}, Total: ₹{r[4]}, Date: {r[5]}")
                elif op == '6':
                    day = input("Enter date (YYYY-MM-DD): ")
                    cur.execute("SELECT SUM(total_price) FROM orders WHERE order_date = %s", (day,))
                    total = cur.fetchone()[0]
                    if total:
                        print(f"💰 Total profit on {day} = ₹{total}")
                    else:
                        print("No orders on this date.")

                elif op == '7':
                    print("🔒 Logging out of Admin Panel.")
                    break

                          
                    
                
                     
                    
                        


                    


         
