1. Configuracion de Base de Datos
Creacion de una base de datos MySQL en Railway.

Obtencion de la variable de entorno DATABASE_URL para la conexion.

2. Desarrollo del Backend (FastAPI)
Implementacion de la API con FastAPI y SQLAlchemy para la gestion de tareas.

Integracion de Autenticacion mediante JWT (JSON Web Tokens) con el endpoint /token.

Configuracion de Logging para el monitoreo de eventos y errores.

Documentacion automatica con OpenAPI/Swagger disponible en la ruta /docs.

3. Desarrollo del Frontend (Vue 3)
Creacion de la interfaz de usuario para consumir los endpoints de la API.

Configuracion de variables de entorno para conectar con la URL de Render.

4. Contenedorizacion
Creacion de un Dockerfile multi-stage para optimizar el tamaño de la imagen del backend.

Configuracion de la ejecucion de Uvicorn en el contenedor.

5. Automatizacion con GitHub Actions
Configuracion de un pipeline de CI (Integracion Continua) que ejecuta tests unitarios con Pytest.

Automatizacion del Build y Push de la imagen Docker hacia Docker Hub tras pasar los tests.

Notificacion automatica a Render mediante un Deploy Hook para actualizar el servicio.

Despliegue automatico del frontend en Vercel tras validar el codigo.

6. Gestion de Secretos y Seguridad
Configuracion de Secrets en GitHub (DOCKERHUB_TOKEN, RENDER_DEPLOY_HOOK, VERCEL_TOKEN) para proteger credenciales.

Uso de variables de entorno para la clave secreta del JWT y credenciales de base de datos.

Capturas
![alt text](image.png)
![alt text](image-2.png)
![alt text](image-3.png)
![alt text](image-1.png)
![alt text](image-4.png)
![alt text](image-5.png)
<img width="1913" height="1040" alt="image" src="https://github.com/user-attachments/assets/1305972a-a336-4aef-872c-0042e7f66951" />
<img width="1905" height="1013" alt="image" src="https://github.com/user-attachments/assets/2a803e42-1121-4fa3-8584-8a159c903364" />
<img width="1909" height="1006" alt="image" src="https://github.com/user-attachments/assets/f808610e-98c2-4b22-a634-08a11ebf7ff8" />
<img width="1913" height="1037" alt="image" src="https://github.com/user-attachments/assets/e5c9fc9d-6e3a-46a9-a764-705e2eeaaced" />
<img width="1905" height="1004" alt="image" src="https://github.com/user-attachments/assets/fa905799-3ae3-4443-871e-23eec6538381" />

https://vercel-y-render.vercel.app

https://vercel-y-render-1.onrender.com
