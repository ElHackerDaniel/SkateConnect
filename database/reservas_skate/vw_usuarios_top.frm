TYPE=VIEW
query=select `u`.`id` AS `id`,ucase(rtrim(`u`.`nombre`)) AS `usuario`,count(`r`.`id`) AS `total` from (`reservas_skate`.`usuarios` `u` left join `reservas_skate`.`reservas` `r` on(`r`.`usuario_id` = `u`.`id`)) group by `u`.`id` order by count(`r`.`id`) desc
md5=fd0141e41745f808037bf53bdfb87c1b
updatable=0
algorithm=0
definer_user=root
definer_host=localhost
suid=2
with_check_option=0
timestamp=0001763255830948287
create-version=2
source=SELECT u.id, UPPER(RTRIM(u.nombre)) AS usuario,\n       COUNT(r.id) AS total\nFROM usuarios u\nLEFT JOIN reservas r ON r.usuario_id = u.id\nGROUP BY u.id\nORDER BY total DESC
client_cs_name=utf8mb4
connection_cl_name=utf8mb4_unicode_ci
view_body_utf8=select `u`.`id` AS `id`,ucase(rtrim(`u`.`nombre`)) AS `usuario`,count(`r`.`id`) AS `total` from (`reservas_skate`.`usuarios` `u` left join `reservas_skate`.`reservas` `r` on(`r`.`usuario_id` = `u`.`id`)) group by `u`.`id` order by count(`r`.`id`) desc
mariadb-version=100432
