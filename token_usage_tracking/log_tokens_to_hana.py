from concurrent.futures import ThreadPoolExecutor
from hdbcli import dbapi

host = "<hana_host>"
port = 443
user = "<hana_user>"
password = "<hana_password>"

# Shared database connection
hana_connection = None
executor = ThreadPoolExecutor(max_workers=2)


def init_db():
    """Initialize the database connection"""
    global hana_connection
    hana_connection = dbapi.connect(
        address=host,
        port=port,
        user=user,
        password=password
    )
    try:    # create metric table if not exists
        cursor = hana_connection.cursor()
        cursor.execute("""
            CREATE COLUMN TABLE TokenLogs (
                Endpoint VARCHAR(255),
                UseCase VARCHAR(255),
                ModelName VARCHAR(255),
                InputTokens INT,
                OutputTokens INT,
                Timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )""")
        hana_connection.commit()
    except:
        print("Table already exists")
    finally:
        cursor.close()
        

def log_tokens_to_hana(endpoint, use_case, model_name, input_tokens, output_tokens):
    """log tokens to the hana database"""
    try:
        # SQL to insert the log data into the table 
        insert_sql = """
        INSERT INTO TokenLogs (Endpoint, UseCase, ModelName, InputTokens, OutputTokens)
        VALUES (?, ?, ?, ?, ?)
        """
        cursor = hana_connection.cursor()
        # Execute the insert statement with provided values
        cursor.execute(insert_sql, (endpoint, use_case, model_name, input_tokens, output_tokens))
        
        # Commit the transaction
        hana_connection.commit()
        print("Log successfully inserted into the table.")
    except Exception as e:
        print(f"Error: {e}")

    finally:
        # Close the cursor
        cursor.close()


def log_tokens(endpoint, use_case, model_name, input_tokens, output_tokens):
    """log tokens via a background thread"""
    executor.submit(log_tokens_to_hana, endpoint, use_case, model_name, input_tokens, output_tokens)
