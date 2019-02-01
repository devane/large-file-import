# large-file-import.py

This is the fastest way I've found of importing more than 1 billion lines in PostgreSQL.

You need to change user/pass/ip/port of postgre connection:

connection = psycopg2.connect(user="postgres", password="somestuff", host="127.0.0.1", port="5433", database="postgres")

You probably need to change the value separator. In my case it is ':'

split_line = line.split(':')

You need to change your insert query. In this case it inserts two values. If your table has more fields you add them here:

sql = b'INSERT into secrets (somestuff1, somestuff2) VALUES %s'

Format of the input file is:

something1:otherthing1<br/>
something2:otherthing2<br/>
something3:otherthing3<br/>
something4:otherthing4<br/>

# Require: 
python 3 and psycopg2

# Use it like this:
./large-file-import.py csv-like-file.txt
