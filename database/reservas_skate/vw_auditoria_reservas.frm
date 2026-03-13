TYPE=VIEW
query=select `a`.`id` AS `id`,`u`.`nombre` AS `usuario`,`a`.`accion` AS `accion`,`a`.`fecha` AS `fecha`,`a`.`descripcion` AS `descripcion` from (`reservas_skate`.`auditoria_reservas` `a` left join `reservas_skate`.`usuarios` `u` on(`u`.`id` = `a`.`usuario_id`)) order by `a`.`fecha` desc
md5=e19e1f4d80fbc5d5a35ec8b11310e02f
updatable=0
algorithm=0
definer_user=root
definer_host=localhost
suid=2
with_check_option=0
timestamp=0001763256211880022
create-version=2
source=SELECT a.id, u.nombre AS usuario, a.accion, a.fecha, a.descripcion\nFROM auditoria_reservas a\nLEFT JOIN usuarios u ON u.id = a.usuario_id\nORDER BY a.fecha DESC
client_cs_name=utf8mb4
connection_cl_name=utf8mb4_unicode_ci
view_body_utf8=select `a`.`id` AS `id`,`u`.`nombre` AS `usuario`,`a`.`accion` AS `accion`,`a`.`fecha` AS `fecha`,`a`.`descripcion` AS `descripcion` from (`reservas_skate`.`auditoria_reservas` `a` left join `reservas_skate`.`usuarios` `u` on(`u`.`id` = `a`.`usuario_id`)) order by `a`.`fecha` desc
mariadb-version=100432
