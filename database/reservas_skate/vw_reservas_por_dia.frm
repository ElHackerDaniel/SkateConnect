TYPE=VIEW
query=select `reservas_skate`.`reservas`.`fecha` AS `fecha`,count(0) AS `total` from `reservas_skate`.`reservas` group by `reservas_skate`.`reservas`.`fecha` order by `reservas_skate`.`reservas`.`fecha`
md5=715a8b2207db884b964301b924e52fcd
updatable=0
algorithm=0
definer_user=root
definer_host=localhost
suid=2
with_check_option=0
timestamp=0001763255632571010
create-version=2
source=SELECT fecha, COUNT(*) AS total\nFROM reservas\nGROUP BY fecha\nORDER BY fecha ASC
client_cs_name=utf8mb4
connection_cl_name=utf8mb4_unicode_ci
view_body_utf8=select `reservas_skate`.`reservas`.`fecha` AS `fecha`,count(0) AS `total` from `reservas_skate`.`reservas` group by `reservas_skate`.`reservas`.`fecha` order by `reservas_skate`.`reservas`.`fecha`
mariadb-version=100432
