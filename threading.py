import psycopg2
import threading
import time

# Database configuration
DB_CONFIG = {
    "dbname": "your_database",
    "user": "your_user",
    "password": "your_password",
    "host": "localhost",
    "port": "5432"
}

# Transaction 1: Read Alice's balance
def transaction_read():
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    
    print("Transaction 1: Starting read transaction...")
    cur.execute("BEGIN;")
    
    cur.execute("SELECT balance FROM accounts WHERE name = 'Alice';")
    balance = cur.fetchone()[0]
    print(f"Transaction 1: Alice's Balance (Before Update): {balance}")

    time.sleep(5)  # Simulating delay to show MVCC effect

    cur.execute("SELECT balance FROM accounts WHERE name = 'Alice';")
    balance_after = cur.fetchone()[0]
    print(f"Transaction 1: Alice's Balance (After Update): {balance_after}")

    cur.execute("COMMIT;")
    cur.close()
    conn.close()
    print("Transaction 1: Committed.\n")

# Transaction 2: Update Alice's balance
def transaction_write():
    time.sleep(2)  # Ensure Transaction 1 starts first

    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    print("Transaction 2: Starting write transaction...")
    cur.execute("BEGIN;")
    
    cur.execute("UPDATE accounts SET balance = 200 WHERE name = 'Alice';")
    print("Transaction 2: Updated Alice's balance to 200.")

    cur.execute("COMMIT;")
    cur.close()
    conn.close()
    print("Transaction 2: Committed.\n")

# Run the simulation
if __name__ == "__main__":
    # Creating two threads to simulate concurrency
    t1 = threading.Thread(target=transaction_read)
    t2 = threading.Thread(target=transaction_write)
    
    t1.start()
    t2.start()
    
    t1.join()
    t2.join()
    
    print("MVCC Simulation Complete.")