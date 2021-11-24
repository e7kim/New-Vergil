-- From https://stackoverflow.com/questions/21738408/postgresql-list-and-order-tables-by-size
select table_name, pg_relation_size(quote_ident(table_name))
from information_schema.tables
where table_schema = 'tg2648'
order by 2;
