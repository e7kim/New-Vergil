"""
Place to test raw SQL
"""

import logging
import os

from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
logging.getLogger('sqlalchemy.pool').setLevel(logging.DEBUG)

engine = create_engine(os.getenv('DATABASE_URI'))

sql_query = '''
SELECT COUNT (*)
FROM instructor
;
'''

with engine.connect() as conn:
    result = conn.execute(text(sql_query))

for row in result:
    print(row)
