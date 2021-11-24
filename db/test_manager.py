# Standard library imports
import os

# Third-party imports
from dotenv import load_dotenv

# Local application imports
from manager import DbManager


load_dotenv()

db = DbManager(db_uri=os.getenv('DATABASE_URI'), query_dir='sql', debug=True)
res = db.run_query('select_all_from_room.sql')
print(res)
