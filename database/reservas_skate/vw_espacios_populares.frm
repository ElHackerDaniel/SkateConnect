TYPE=VIEW
query=select `e`.`id` AS `id`,`e`.`nombre` AS `nombre`,count(`r`.`id`) AS `total` from (`reservas_skate`.`espacios` `e` left join `reservas_skate`.`reservas` `r` on(`r`.`espacio_id` = `e`.`id`)) group by `e`.`id` order by count(`r`.`id`) desc
md5=ab56d0891c9cb6a4d79c8229bd73b646
updatable=0
algorithm=0
definer_user=root
definer_host=localhost
suid=2
with_check_option=0
timestamp=0001763255675662325
create-version=2
source=SELECT e.id, e.nombre, COUNT(r.id) AS total\nFROM espacios e\nLEFT JOIN reservas r ON r.espacio_id = e.id\nGROUP BY e.id\nORDER BY total DESC
client_cs_name=utf8mb4
connection_cl_name=utf8mb4_unicode_ci
view_body_utf8=select `e`.`id` AS `id`,`e`.`nombre` AS `nombre`,count(`r`.`id`) AS `total` from (`reservas_skate`.`espacios` `e` left join `reservas_skate`.`reservas` `r` on(`r`.`espacio_id` = `e`.`id`)) group by `e`.`id` order by count(`r`.`id`) desc
mariadb-version=100432
