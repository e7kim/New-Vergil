SELECT
   table_name,
   column_name,
   data_type
FROM
   information_schema.columns
WHERE
   table_name = 'instructor' AND
   table_schema = 'tg2648';
