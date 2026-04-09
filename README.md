# 🍽️ RestaurantPro - Sistema POS y Gestión de Restaurantes

RestaurantPro es un completo sistema web de Punto de Venta (POS) y gestión integral para restaurantes, pollerías, cafeterías y negocios gastronómicos. Está diseñado para optimizar el flujo de trabajo entre los clientes, los mozos, la caja y la cocina, utilizando tecnología en tiempo real.

## ✨ Características Principales

* **🔐 Sistema de Roles Inteligente:**
  * **Administrador:** Acceso total, reportes gerenciales, gestión de personal y configuración de la empresa.
  * **Cajero:** Control de la caja, cobros, facturación e historial de pedidos.
  * **Mozo:** Interfaz optimizada (Monitor POS) para tomar pedidos rápidamente y ver el estado de las mesas.
  * **Cocinero / Chef:** Pantalla exclusiva de cocina. Solo ve los pedidos pendientes y emite alertas cuando están listos.
* **📱 Carta Digital y Autoservicio (QR):**
  * Generación automática de Códigos QR por mesa.
# 🍽️ RestaurantPro: Sistema de Gestión de Restaurantes (SaaS Premium)

RestaurantPro es una plataforma integral diseñada para modernizar la operación de restaurantes, cafeterías y bares. Con una interfaz **SaaS Premium** de alta fidelidad, el sistema ofrece una experiencia de usuario fluida, segura y visualmente impactante.

---

## 💎 Características Principales

### 📊 Dashboard Administrativo 360°
- **KPIs en Tiempo Real:** Visualización de ingresos del día, pedidos procesados, platos en cocina y aforo libre.
- **Gráficos Dinámicos:** Seguimiento semanal de tráfico financiero mediante Chart.js.
- **Registro Maestro:** Auditoría completa de todos los tickets y anulaciones del sistema.

### 🍱 Toma de Pedidos (POS Moderno)
- **Interfaz Reestructurada:** Diseño ergonómico con catálogo a la izquierda (80% de ancho) y cuenta/ticket dinámico a la derecha.
- **Gestión Multi-Tipo:** Soporte nativo para **Mesa (Salón)**, **Para Llevar (Takeaway)** y **Envío (Delivery)**.
- **Stock Inteligente:** Alertas visuales cuando un producto tiene pocas unidades.

### 👨‍🍳 SVC (Sistema de Visualización de Cocina - KDS)
- **Monitoreo en Tiempo Real:** Los cocineros reciben los pedidos instantáneamente mediante WebSockets.
- **Semáforo de Tiempos:** Alertas visuales (Verde/Amarillo/Rojo) según el tiempo de espera del plato.
- **Gestión de Estados:** Flujo de trabajo optimizado: *Cola -> Fuego -> ¡Listo!*.

### 💰 Central de Caja y Operaciones
- **Control de Sesiones:** Apertura y cierre de caja con validación de fondo.
- **Gestión de Egresos:** Registro detallado de salidas de dinero (gastos técnicos/compras).
- **Seguridad RBAC:** Roles definidos para **Administrador**, **Mozo** y **Cocinero** con acceso restringido.

---

## 🛠️ Requisitos Técnicos

Para implementar RestaurantPro de manera local, asegúrate de tener:
- **Python 3.10** o superior.
- **XAMPP** (Servidor MySQL/MariaDB).
- **Git** (Opcional, para clonar el repositorio).

---

## 🚀 Guía de Instalación Local

Sigue estos pasos para poner el sistema en marcha en una nueva computadora:

### 1. Clonar o Copiar el Proyecto
Descarga el código fuente y colócalo en tu directorio de preferencia (Ej: `C:\xampp\htdocs\restaurantpro`).

### 2. Crear un Entorno Virtual
Abre una terminal en la carpeta del proyecto y ejecuta:
```bash
python -m venv .venv
```
Activa el entorno:
primero ejecuta este comando en poweshell como usuario normal
"Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser"
- **Windows:** `.venv\Scripts\activate`
- **Linux/Mac:** `source .venv/bin/activate`

### 3. Instalar Dependencias
Instala todas las librerías necesarias ejecutando:
```bash
pip install -r requirements.txt
```

### 4. Configuración del Servidor MySQL (XAMPP)
1. Abre el **XAMPP Control Panel** e inicia los módulos **Apache** y **MySQL**.
2. Ingresa a [http://localhost/phpmyadmin](http://localhost/phpmyadmin).
3. Crea una nueva base de datos llamada `restaurantpro` con cotejamiento `utf8mb4_general_ci`.

### 5. Configuración de Variables de Entorno
Crea un archivo llamado `.env` en la raíz del proyecto (o edita el existente) con el siguiente formato:
```env
SECRET_KEY=tu_clave_secreta_aqui
DATABASE_URL=mysql+pymysql://root:@localhost/restaurantpro
```
*(Nota: Si tu usuario de MySQL tiene contraseña, cámbialo a: `root:CONTRASEÑA@localhost/restaurantpro`)*

### 6. Inicializar la Base de Datos
Para crear las tablas automáticamente, puedes ejecutar:
```bash
python run.py
```
*(El sistema verificará y creará las tablas al primer arranque. Si tienes migraciones pendientes, ejecuta `python migrate.py`)*.

---

## 💻 Ejecución del Sistema

Para iniciar el servidor de desarrollo, simplemente corre:
```bash
python run.py
```
El sistema estará disponible en tu red local:
- **Acceso Local:** [http://127.0.0.1:5000](http://127.0.0.1:5000)
- **Acceso Red Local:** `http://TU_IP_LOCAL:5000` (Ideal para tablets de mozos y pantallas de cocina).

---

## 🔐 Credenciales por Defecto (Seguridad)
El sistema utiliza el decorador `@role_required` para proteger áreas sensibles. Asegúrate de crear el primer usuario administrativo o verificar que la base de datos tenga los registros iniciales.

---

## 📁 Estructura del Proyecto
- **/app**: Lógica principal (Rutas, Modelos, Estáticos, Plantillas).
- **/database**: Almacenamiento y esquemas.
- **/app/static/uploads**: Directorio donde se almacenan las fotos de los productos.
- **run.py**: Punto de entrada del servidor Flask + SocketIO.

---
**Desarrollado con ❤️ por el equipo de RestaurantPro.**



