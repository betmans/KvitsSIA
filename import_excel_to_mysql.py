# import pandas as pd
# import mysql.connector
# from sqlalchemy import create_engine

# # MySQL connection details
# db_user = "root"  # Replace with your MySQL username
# db_password = "yourpassword"  # Replace with your MySQL password
# db_host = "localhost"  # Host, typically 'localhost' or '127.0.0.1'
# db_name = "store_db"  # Your database name

# # Connect to MySQL using SQLAlchemy
# engine = create_engine(f"mysql+mysqlconnector://{db_user}:{db_password}@{db_host}/{db_name}")

# # Load Excel file
# excel_file = "C:\\Users\\Oskar\\Desktop\\KvitsSIA\\Sortiments KVITS 2024.xls"
# df = pd.read_excel(excel_file)

# # Save data to MySQL
# df.to_sql("products", engine, if_exists="append", index=False)

# print("Data imported successfully!")

#& "C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe" -u root -p


# import mysql.connector

# # Replace with your MySQL credentials
# conn = mysql.connector.connect(
#     host="localhost",
#     user="root",
#     password="betHESDA",
#     database="Kvits"
# )

# if conn.is_connected():
#     print("Connected to MySQL successfully!")
# else:
    # print("Failed to connect.")








# import pandas as pd
# from sqlalchemy import create_engine

# # Database credentials
# db_user = "root"
# db_password = "4859"
# db_host = "localhost"
# db_name = "kvits"

# # Create SQLAlchemy engine (uses PyMySQL as driver)
# engine = create_engine(f"mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}")

# # Read Excel file
# excel_file = "C:\\Users\\Oskar\\Desktop\\KvitsSIA\\Sortiments KVITS 2024.xls" # Change to your actual file name
# df = pd.read_excel(excel_file)

# # Write DataFrame to MySQL table
# df.columns = df.columns.str.replace(' ', '_').str.replace('(+40%)', '40_percent')
# df['Pasūtījuma_kods'] = df['Pasūtījuma_kods'].str.replace('.', '', regex=False)
# # Preprocessing the 'Veikala_plaukta_cena_40_percent' column to clean data
# df['Veikala_plaukta_cena_40_percent'] = df['Veikala_plaukta_cena_40_percent'].str.replace(',', '.').str.strip().astype(float)

# df.to_sql("katalogs", con=engine, if_exists="append", index=False)

# print("Excel file imported successfully into MySQL!")