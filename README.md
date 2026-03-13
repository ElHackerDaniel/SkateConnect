🛹 SkateConnect
=============
SkateConnect es una aplicación web para la gestión y reserva de espacios de skate.
Permite a los usuarios reservar pistas o espacios disponibles, cancelar reservas y consultar su historial, mientras que los administradores pueden gestionar el sistema y visualizar reportes.

El objetivo del proyecto es ofrecer una plataforma simple para organizar reservas de espacios deportivos, evitando conflictos de horarios y permitiendo una mejor administración.

🚀 Características
-------------
- 🔐 Autenticación de usuarios
  - Registro
  - Inicio de sesión
- 👥 Sistema de roles
  - ADMIN → control total del sistema
  - DIRECTORIO → acceso a reportes y gestión limitada
  - USUARIO → puede reservar, cancelar y ver su historial
- 🛹 Gestión de reservas
  - Crear reservas
  - Cancelar reservas
  - Seleccionar espacios disponibles
  - Definir número de participantes
- 🧾 Facturación
  - Generación de facturas en PDF
  - Historial de facturación por usuario
- 📊 Panel de administración
  - Visualización de reservas
  - Reportes del sistema

🏗️ Tecnologías utilizadas
-------------
###Backend

- Python
- Flask
- MySQL

###Frontend

- HTML5
- CSS3
- JavaScript

###Librerías

- ReportLab (generación de PDF) 

⚙️ Instalación
-------------
###Clonar el repositorio

`$ git clone https://github.com/ElHackerDaniel/SkateConnect.git`
`$ cd skateconnect`

###Crear entorno virtual (opcional)
`$ python -m venv venv`

Activarlo:

Windows

`$ venv\Scripts\activate`

Linux / Mac

`$ source venv/bin/activate`

###Instalar dependencias

`$ pip install flask mysql-connector-python reportlab`
###Configurar la base de datos
Editar el archivo:

`config/db_config.py`

Con tus credenciales de MySQL.

Ejemplo:

```javascript
host = "localhost"
user = "root"
password = ""
database = "skateconnect"
```
###Ejecutar el proyecto
`python app.py`

Abrir en el navegador:

`http://localhost:5000`

En esta parte podrias ir a ver las instructions.txt para el link https

👤 Roles del sistema
-------------
| Rol      | Permisos |
| :---------: | :-----:|
| Admin  | Gestiona usuarios, reservas y reportes |
| Directorio     |  Visualiza reportes |
| Usuario      | Realiza reservas y consulta historial |
###📄 Generación de facturas
Cada reserva genera una factura en PDF que incluye:
- ID de la reserva
- Usuario
- Espacio reservado
- Fecha
- Hora
- Participantes

Las facturas se guardan en:

`/facturas`
###📌 Posibles mejoras futuras
- Pagos en línea
- Notificaciones por correo
- Calendario visual de reservas
- Panel de estadísticas
- API REST

###👨‍💻 Autor
Proyecto desarrollado como parte de aprendizaje en desarrollo web con Python y bases de datos.
Att: ElHackerDaniel
