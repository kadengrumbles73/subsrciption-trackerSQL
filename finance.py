import sqlite3

def main():
    init_db()
    # seed db is for dummy data
    #seed_db()
    choice = ""
    #toggle_sub_status("Locker Room", True) # test
    
    while True:
        
        monthly = get_monthly_cost()
        daily = burn_rate_calc()
        print("\n" + "="*30)
        print("   PERSONAL FINANCE TRACKER")
        print(f"   Monthly Burn: ${monthly:.2f}")
        print(f"   Daily Burn:   ${daily:.2f}")
        print("="*30)
        print("1. View All Subscriptions")
        print("2. Add New Subscription")
        print("3. Cancel Subscription")
        print("4. Renew Subscription")
        print("5. Pay Subscription")
        print("6. View payment history")
        print("7. Exit")
        
        choice = int(input("What would you like to do? " ))
        if choice == 1:
            display_subscriptions()
        
        if choice == 2:
            add_subscription()
        
        if choice == 3:
            user_input = input("What subscription would you like to cancel? ")
            toggle_sub_status(user_input, False )
        
        if choice == 4:
            user_input = input("What subscription would you like to renew? ")
            toggle_sub_status(user_input, True )

        if choice == 5:
            pay_subscription()

        if choice == 6:
            display_payments()
            
        if choice == 7:
            break

def init_db():
    #set up the tables of db
    subscriptions_command = """CREATE TABLE IF NOT EXISTS subscriptions(
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL UNIQUE, -- like netflix
        category TEXT NOT NULL,-- like tv
        is_active INTEGER NOT NULL DEFAULT 1, -- 1 for active 0 for inactive
        monthly_cost REAL NOT NULL CHECK(monthly_cost >= 0), -- 10.99
        billing_day INTEGER CHECK(billing_day BETWEEN 1 AND 31)); -- day of month account gets charged
        """ 

    payment_history_command = """CREATE TABLE IF NOT EXISTS payment_history (
        id INTEGER PRIMARY KEY,
        subscription_id INTEGER NOT NULL, -- foreign key
        amount_paid REAL NOT NULL CHECK(amount_paid >= 0), -- 10.99
        payment_date TEXT NOT NULL, -- Format: YYYY-MM-DD
        FOREIGN KEY (subscription_id) REFERENCES subscriptions (id));"""

    with sqlite3.connect('finance.db') as conn:
        conn.execute(subscriptions_command)
        conn.execute(payment_history_command)

def seed_db():
        dummy_subscriptions = [
            (1, "Netflix", "Streaming", 10.99, 15),
            (0, "Amazon Music", "Music", 5.59, 11),
            (1,"Locker Room", "Health", 55.67, 10)
        ]
        
        dummy_payments = [
            (1, 10.99, "2026-01-12"),
            (3, 55.67, "2026-01-09"),
            (1, 10.99, "2026-02-11"),
            (3, 55.67, "2026-02-10"),
            (1, 10.99, "2026-03-07"),
            (3, 55.67, "2026-03-08"),
            (1, 10.99, "2026-04-12"),
            (3, 55.67, "2026-04-05"),
        ]
        
        with sqlite3.connect('finance.db') as conn:    
            cursor = conn.cursor()
            # bring it all at once instead of one at a time
            cursor.executemany("""INSERT OR IGNORE INTO subscriptions (is_active, name, category, monthly_cost, billing_day) VALUES(?, ?, ?, ?, ?)""", dummy_subscriptions)
            cursor.executemany("""INSERT OR IGNORE INTO payment_history (subscription_id, amount_paid, payment_date) VALUES(?, ?, ?)""", dummy_payments)
            
def get_monthly_cost():
    with sqlite3.connect('finance.db') as conn:    
        cursor = conn.cursor()
        # get the sum of the monthly cost using SQL
        monthly_cost_q = """SELECT SUM(monthly_cost) 
                       FROM subscriptions
                       WHERE is_active = 1"""
        cursor.execute(monthly_cost_q)
        result = cursor.fetchone() # brings query to python
        
        return result[0] if result[0] is not None else 0.0 # make sure if db is empty it sends a zero and not none

def burn_rate_calc():
    # If there is no cost, the burn rate is 0. 
    # This prevent None / 30 error.
    monthly_cost = get_monthly_cost()
    if monthly_cost is None:
        return 0.0
    
    burn_rate = monthly_cost / 30
    return burn_rate

def toggle_sub_status(sub_name, make_active=True):
    new_status = 1 if make_active else 0 # update db
    with sqlite3.connect('finance.db') as conn:
        sql = "UPDATE subscriptions SET is_active = ? WHERE name = ?"
        conn.execute(sql, (new_status, sub_name))
        status_text = "Active" if make_active else "Inactive" # display sta tus in app w
        print(f"\nUpdate successful: {sub_name} is {status_text}.")

def add_subscription():
    name = str(input("What is the name of your new subscription? ")).upper()
    cat = str(input("What category does your subscription fall in? ")).upper()
    cost = float(input("How much does your subscription cost per month? "))
    day = int(input("What day does the subscription renew? " ))
    # prompt data from user then inputed into tuple to put through sql insert statement
    
    with sqlite3.connect("finance.db") as conn:
        cursor = conn.cursor()
    new_subscription = (name, cat, 1, cost, day)
    cursor.execute("""INSERT OR IGNORE INTO subscriptions (name, category, is_active, monthly_cost, billing_day) VALUES(?, ?, ?, ?, ?)""", new_subscription)
    conn.commit()
    
def display_subscriptions():
    with sqlite3.connect('finance.db') as conn:
        cursor = conn.cursor()
        # Get the  data to show the user
        cursor.execute("SELECT name, category, monthly_cost, is_active FROM subscriptions")
        rows = cursor.fetchall()
            # headerr
        print(f"\n{'Name'} {'Category'} {'Cost'} {'Status'}")
        print("-" * 50)
        # loop through the list of tuples
        for row in rows:
            # Convert the binary in the DB t words
            status = "Active" if row[3] == 1 else "Inactive"
            print(f"{row[0]} {row[1]} ${row[2]} {status:}")  

def pay_subscription():
    sub_name = input("Which subscription did you just pay? ").upper()

    with sqlite3.connect("finance.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM subscriptions WHERE name = ?", (sub_name,))
        result = cursor.fetchone()
        
        if result is None:
            print(f"\nError: '{sub_name}' not found. Please check the name and try again.")
            return # This exits the function early so the program don't crash

        sub_id = result[0]
        
        try:
            amount = float(input(f"Confirm the payment amount for {sub_name}: "))
        except:
            print("Invalid amount. Please enter another number")
            return
        
        pay_date = input("Enter date (YYYY-MM-DD) or press Enter for today: ")
        if not pay_date:
            from datetime import date
            pay_date = str(date.today())
            
        sql = """INSERT INTO payment_history (subscription_id, amount_paid, payment_date) 
                        VALUES (?, ?, ?)"""
        cursor.execute(sql, (sub_id, amount, pay_date))
        print(f"\nSuccessfully recorded ${amount:.2f} payment for {sub_name}!")

def display_payments():
    with sqlite3.connect("finance.db") as conn:
        cursor = conn.cursor()
        
        sql_join = """
            SELECT s.name, p.amount_paid, p.payment_date
            FROM payment_history AS p
            JOIN subscriptions AS s ON p.subscription_id = s.id"""
        
        cursor.execute(sql_join)
        rows = cursor.fetchall()
        
        if not rows:
            print("\nNo payment history found.")
            return

        print(f"\n{'Service'} {'Amount'} {'Date Paid'}")
        print("-" * 40)
        
        for row in rows:
            print(f"{row[0]} ${row[1]} {row[2]}")

if __name__ == "__main__":
    main()