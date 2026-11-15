import sqlite3

db_list = ["retail_app.db", "retailApp.db"]

for db_name in db_list:
    print(f"\n📂 Checking {db_name}:")
    try:
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        if tables:
            print("✅ Tables found:", tables)
        else:
            print("❌ No tables found.")
        conn.close()
    except Exception as e:
        print("⚠️ Error:", e)
