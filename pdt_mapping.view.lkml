explore: pdt_mapping {}

view: pdt_mapping {
  derived_table: {
    sql:
      SELECT 'pdt_common_name' name, '${pdt_common_name.SQL_TABLE_NAME}' internal_name
    ;;
#        UNION SELECT 'pdt_2_common_name', '${pdt_2_common_name.SQL_TABLE_NAME}'
#        UNION SELECT 'pdt_3_common_name', '${pdt_3_common_name.SQL_TABLE_NAME}'
  }

  dimension: name {}
  dimension: internal_name {}

  dimension: view_sql_mysql {
    sql: CONCAT('DROP TABLE IF EXISTS pdt.', ${name}, '; CREATE VIEW pdt.', ${name} , ' AS ',
          'SELECT * FROM ' , ${internal_name} , ' WITH NO SCHEMA BINDING')
          ;;
  }

  dimension: view_sql_redshift {
    sql: 'CREATE OR REPLACE VIEW pdt.' || ${name} || ' AS '
          'SELECT * FROM ' || ${internal_name} || ' WITH NO SCHEMA BINDING'
          ;;
  }
}
