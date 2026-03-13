TYPE=TRIGGERS
triggers='CREATE DEFINER=`root`@`localhost` TRIGGER trg_reserva_insert\nAFTER INSERT ON reservas\nFOR EACH ROW\nBEGIN\n    INSERT INTO auditoria_reservas(reserva_id, usuario_id, accion, descripcion)\n    VALUES (NEW.id, NEW.usuario_id, \'CREAR\', \n            CONCAT(\'Se creó una reserva para el espacio \', NEW.espacio_id,\n                   \' el día \', NEW.fecha, \n                   \' desde \', NEW.hora_inicio, \' hasta \', NEW.hora_fin));\nEND' 'CREATE DEFINER=`root`@`localhost` TRIGGER trg_reserva_update\nAFTER UPDATE ON reservas\nFOR EACH ROW\nBEGIN\n    INSERT INTO auditoria_reservas(reserva_id, usuario_id, accion, descripcion)\n    VALUES (NEW.id, NEW.usuario_id, \'ACTUALIZAR\',\n            CONCAT(\'La reserva fue modificada. Nuevo horario: \',\n                   NEW.hora_inicio, \' - \', NEW.hora_fin));\nEND' 'CREATE DEFINER=`root`@`localhost` TRIGGER trg_reserva_delete\nAFTER DELETE ON reservas\nFOR EACH ROW\nBEGIN\n    INSERT INTO auditoria_reservas(reserva_id, usuario_id, accion, descripcion)\n    VALUES (OLD.id, OLD.usuario_id, \'ELIMINAR\',\n            \'La reserva fue eliminada del sistema\');\nEND'
sql_modes=1098907648 1098907648 1098907648
definers='root@localhost' 'root@localhost' 'root@localhost'
client_cs_names='utf8mb4' 'utf8mb4' 'utf8mb4'
connection_cl_names='utf8mb4_unicode_ci' 'utf8mb4_unicode_ci' 'utf8mb4_unicode_ci'
db_cl_names='utf8_general_ci' 'utf8_general_ci' 'utf8_general_ci'
created=1763256158257703 1763256191921519 1763256202033046
