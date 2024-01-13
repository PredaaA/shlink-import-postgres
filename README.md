# shlink-import-postgres

So I've had to import data from an existing Shlink instance to a new one... more specifically, changing the database from MariaDB to Postgres.

There is a [tool made for that](https://shlink.io/documentation/advanced/import-short-urls/#shlink-instance), but the issue is that it's very slow when you have many short urls saved, because it is calling the rest API to retrieve 50 entries, which by itself already takes 3-5 seconds. Considering I've had millions of entries, this would've take... way too much time.

So I decided to make that little script, it takes credentials from the current MariaDB and the Postgres one.  
It will then proceed by doing a big select from the short_urls table (on MariaDB), and insert the result to Postgres.

It's taking only a few selected rows (author_api_key_id, original_url, short_code, date_created) since I didn't care about the other ones.
