# 🤖 RPA - Consulta Judicial y Envío de Documentos

**Prueba Técnica | Parametrizador / Desarrollador de Automatizaciones RPA**
**TCC - Tecnología, Consultoría y Capacitación | Departamento DIA**

---

## Tabla de Contenido

1. [Herramienta utilizada y versión](#1-herramienta-utilizada-y-versión)
2. [Resumen de la solución](#2-resumen-de-la-solución)
3. [Cómo configurar y ejecutar el bot](#3-cómo-configurar-y-ejecutar-el-bot)
4. [Decisiones técnicas clave](#4-decisiones-técnicas-clave)
5. [Limitaciones y trabajo pendiente](#5-limitaciones-y-trabajo-pendiente)

---

## 1. Herramienta utilizada y versión

| Atributo | Detalle |
|----------|---------|
| **Herramienta** | Rocketbot Studio |
| **Versión** | 2025 |
| **Lenguaje base** | Python 3.7 |
| **Modalidad** | Community Edition |

### ¿Por qué Rocketbot Studio?

Para el desarrollo de esta automatización se eligió **Rocketbot Studio** por las siguientes razones técnicas y de viabilidad:

- **Acceso inmediato y sin fricción de licenciamiento:** Rocketbot ofrece una versión Community con todas las capacidades necesarias para este flujo, sin restricciones de prueba ni de licencia Enterprise que limitarían el desarrollo en el tiempo disponible.
- **Módulo nativo de Web Scraping:** Rocketbot incluye un módulo dedicado para interacción web con soporte a XPath dinámicos, lo que resulta ideal para la navegación por el portal de la Rama Judicial, cuyos elementos HTML son dinámicos y requieren selectores robustos.
- **Integración nativa con bases de datos SQLite:** No requiere codificación adicional para conectar, leer y escribir en bases de datos relacionales locales.
- **Módulo Gmail nativo:** La lectura de correos IMAP y el envío SMTP están encapsulados en un módulo oficial, evitando configuraciones manuales de protocolos.
- **Registro de logs y manejo de credenciales de Windows:** Capacidades integradas que facilitan el registro de auditoría y la gestión segura de contraseñas sin exponer credenciales en el código.

> **Otras herramientas consideradas y descartadas:**
> - **UiPath**: Requiere licencia Enterprise paga; no existe versión gratuita funcional para este tipo de flujo completo.
> - **Automation Anywhere**: Sin acceso disponible a cuentas Community al momento del desarrollo.
> - **Power Automate Desktop**: La versión gratuita tiene limitaciones para flujos complejos con bases de datos y lógica transaccional.
> - **n8n**: Requiere codificación más compleja para la interacción con elementos web dinámicos mediante XPath.

---

## 2. Resumen de la solución

### Descripción del flujo paso a paso

El bot automatiza la consulta de procesos judiciales de personas naturales en el portal de la Rama Judicial, descarga el historial de actuaciones y notifica los resultados por correo electrónico.

| Paso | HU | Descripción |
|------|----|-------------|
| 1 | Inicialización | El bot `Main_ConsultaJudicial` carga variables de configuración desde la tabla `B01_ConsultaJudicial_Config`, envía notificación de inicio y valida las banderas de ejecución del día en `B01_ConsultaJudicial_Flags`. Si no hay ejecuciones del día, inicializa todas las HU en estado pendiente. |
| 2 | HU01 | Se conecta al correo Gmail, extrae el nombre de la persona desde el cuerpo del correo y registra el caso en `B01_ConsultaJudicial_Transacciones` con estado `Pending`. |
| 3 | HU02 | Abre Chrome, navega a la Rama Judicial, selecciona "Todos los Procesos" y "Persona Natural", ingresa el nombre y ejecuta la búsqueda. Identifica el **sexto (6°) resultado** de la tabla, hace clic en el número de radicación y descarga el historial de actuaciones en CSV. |
| 4 | HU02 | Actualiza la tabla de transacciones con el número de radicado, la ruta del archivo descargado y la URL de descarga. |
| 5 | HU03 | Envía un correo HTML al destinatario configurado con el documento adjunto, el nombre consultado, el radicado y la URL del proceso. Marca la transacción como `Processed`. |

### Diagrama del flujo (ASCII)

```
┌─────────────────────────────────────────────────────────────────┐
│                    Main_ConsultaJudicial                        │
│                                                                 │
│  [Inicio] → FUN_ConfigVars → Notificación Inicio               │
│          ↓                                                      │
│  Validar banderas del día (B01_ConsultaJudicial_Flags)         │
│  ¿Hay HU pendientes? ──No──→ Inicializar banderas              │
│          ↓ Sí                                                   │
└─────────────────────┬───────────────────────────────────────────┘
                      │
          ┌───────────▼───────────┐
          │  HU01_Recepcion       │
          │  _Solicitudes         │
          │                       │
          │  Conectar a Gmail     │
          │  Leer correo nuevo    │
          │  Extraer nombre       │
          │  (Body del correo)    │
          │  Guardar → Pending    │
          └───────────┬───────────┘
                      │ ✔ OK  (3 reintentos en error)
          ┌───────────▼───────────┐
          │  HU02_Busqueda        │
          │  _RamaJudicial        │
          │                       │
          │  Abrir Chrome         │
          │  Navegar → URL        │
          │  Filtrar: Natural     │
          │  Ingresar nombre      │
          │  Click CONSULTAR      │
          │  Espera inteligente   │
          │  Contar filas ≥ 6?    │
          │  Click fila 6°        │
          │  Descargar CSV        │
          │  Guardar radicado     │
          │  y URL en BD          │
          └───────────┬───────────┘
                      │ ✔ OK  (3 reintentos en System Exception)
          ┌───────────▼───────────┐
          │  HU03_Notificacion    │
          │  _Cierre              │
          │                       │
          │  Construir correo     │
          │  HTML con adjunto     │
          │  Enviar a destinat.   │
          │  Marcar → Processed   │
          └───────────┬───────────┘
                      │
                 [Fin del Bot]

  Excepciones:
  ├── Business_Exception → Registra en BD, continúa flujo
  └── System_Exception   → Registra en BD, 3 reintentos, captura screenshot
```

### Arquitectura modular

```
Main_ConsultaJudicial (Orquestador)
├── FUN_ConfigVars -> Carga variables desde B01_ConsultaJudicial_Config
├── HU01_Recepcion_Solicitudes
├── HU02_Busqueda_RamaJudicial
└── HU03_Notificacion_Cierre
```

### Estructura de base de datos

```sql
-- Variables de configuración del bot
B01_ConsultaJudicial_Config  (id, Name, Prod, Dev, Description)

-- Control de ejecución por historia de usuario
B01_ConsultaJudicial_Flags   (hu, taskname, attempts, finished, date)

-- Cola de transacciones con estados
B01_ConsultaJudicial_Transacciones (
    id, strNombreConsultar, strRadicado, strRutaDocumento,
    Status, ProcessDate, Notes, CorrelationId, UrlWeb
)
-- Status: Pending | Processed | Business_Exception | System_Exception
```

---

## 3. Cómo configurar y ejecutar el bot

### Requisitos previos

| Requisito | Detalle |
|-----------|---------|
| Sistema Operativo | Windows 10 / 11 |
| Python | 3.7 o superior |
| Navegador | Google Chrome actualizado (>120) |
| Conectividad | Acceso sin bloqueos al dominio `consultaprocesos.ramajudicial.gov.co` |
| Correo | Cuenta Gmail con contraseña de aplicación habilitada (2FA activo) |
| Disco | Permisos de lectura/escritura en disco `C:\` |

### Estructura del proyecto

```
C:\Main_ConsultaJudicial
├── docs\               # PDD, documentos de prueba y viabilidad
├── Downloads\          # Carpeta temporal para descarga de CSVs
├── logs\
│   └── 2026\
│       └── 05\         # Logs por día: Log_Audit_2026-05-15.txt
├── modules\            # Módulos Rocketbot (SQLite, Gmail, System++, etc.)
├── resources\
│   ├── InitAuto.py     # Script de instalación y configuración
│   ├── EndAuto.py      # Script de limpieza del ambiente
│   ├── setup_db.sql    # Script de creación de tablas
│   └── *.json          # Backup de variables del bot
├── robots\
│   ├── Preview v2.0\   # ⬅ Versión estable actual (Robot.db)
│   └── Preview_0.1\    # Versión inicial de desarrollo
└── screenshot\
    └── 2026\
        └── 05\         # Capturas de errores por mes
```

### Paso 1 — Obtener la contraseña de aplicación Gmail

Contacte al desarrollador **Jonathan Rincón** vía WhatsApp para recibir la contraseña de aplicación del correo Gmail configurado para el bot. Esta contraseña se utilizará en el siguiente paso.

> ⚠️ **Importante:** No use la contraseña personal de Gmail. Debe ser una *App Password* generada desde la configuración de seguridad de Google con 2FA activo.

### Paso 2 — Ejecutar el script de inicialización

1. Abra una terminal (CMD o PowerShell) **como Administrador**.
2. Navegue a la carpeta de recursos:
   ```
   cd C:\Main_ConsultaJudicial\resources
   ```
3. Abra el archivo `InitAuto.py` con un editor de texto y localice esta línea:
   ```python
   GMAIL_PASSWORD = ""  # Ingresar la contraseña de aplicacion de gmail
   ```
4. Ingrese entre las comillas la contraseña de aplicación recibida.
5. Guarde el archivo y ejecute:
   ```
   python InitAuto.py
   ```

Este script realizará automáticamente:
- Instalación de la variable global con la **ruta de acceso a la base de datos SQLite**.
- Clonación/descarga del repositorio del proyecto desde GitHub.
- Configuración de la **credencial `Gmail_ConsultaJudicial`** en el Administrador de Credenciales de Windows (usuario y contraseña del correo).

### Paso 3 — Instalar Rocketbot Studio

1. Descargue Rocketbot Studio v2025 desde:
   ```
   https://rocketbot.com/es/rocketbot-studio-rpa/
   ```
   En la sección inferior de la página, busque la opción **Rocketbot v2025**.

2. Descomprima la carpeta descargada. Se recomienda colocarla en la raíz del disco `C:\`:
   ```
   C:\roc_studio\Rocketbot\
   ```

### Paso 4 — Instalar los módulos del bot

Copie **todos los módulos** que se encuentran en:
```
C:\Main_ConsultaJudicial\modules\
```
Hacia la carpeta de módulos de Rocketbot:
```
C:\roc_studio\Rocketbot\modules\
```

> Los módulos incluyen las dependencias necesarias: SQLite, Gmail, System++, entre otros.

### Paso 5 — Importar y ejecutar el bot

1. Ejecute Rocketbot Studio **como Administrador**:
   ```
   C:\roc_studio\Rocketbot\rocketbot.exe
   ```
2. En la pantalla principal, haga clic en el botón **Importar**.
3. Seleccione el archivo del proyecto:
   ```
   C:\Main_ConsultaJudicial\robots\Preview v2.0\Robot.db
   ```
4. Espere a que el bot cargue completamente en el Studio.
5. Haga clic en el botón **▶ Ejecutar** para iniciar el proceso.

### Paso 6 — Limpiar el ambiente (opcional)

Para eliminar las credenciales y variables globales configuradas por el script de inicialización, ejecute:
```
python C:\Main_ConsultaJudicial\resources\EndAuto.py
```

### Variables de configuración

Las siguientes variables están parametrizadas en la tabla `B01_ConsultaJudicial_Config` de la base de datos. No hay valores hardcodeados en el flujo del bot:

| Variable | Descripción |
|----------|-------------|
| Correo de entrada | Bandeja de Gmail donde llegan las solicitudes con el nombre a consultar |
| Ruta base de datos | Ruta absoluta al archivo SQLite `datos.db` |
| Credencial Gmail | Nombre de la credencial Windows: `Gmail_ConsultaJudicial` |
| URL Rama Judicial | `https://consultaprocesos.ramajudicial.gov.co/Procesos/NombreRazonSocial` |
| Correos de notificación | Destinatarios para envío de resultados y alertas de error |
| Ruta de logs | Carpeta donde se almacenan los archivos de auditoría |
| Ruta de descargas | Carpeta `Downloads\` para archivos CSV descargados |
| Plantilla HTML correo inicio | HTML/CSS del correo de notificación de inicio de ejecución |
| Plantilla HTML correo error | HTML/CSS del correo de alerta de error |
| Plantilla HTML correo cierre | HTML/CSS del correo de finalización exitosa |
| ID de ejecución | CorrelationId único generado por ejecución para trazabilidad |
| Ruta screenshots | Carpeta `screenshot\` para capturas de pantalla de errores |

> 💡 **Agregar imágenes al README:** Para enriquecer visualmente esta documentación en GitHub, agregue imágenes con la sintaxis `![Descripción](ruta/imagen.png)`. Se recomienda crear una carpeta `/docs/img/` dentro del repositorio y referenciar las capturas del flujo, pantallas de configuración y ejecución del bot desde allí.

---

## 4. Decisiones técnicas clave

### 4.1 Estrategia para identificar el sexto resultado

La identificación del sexto registro de la tabla de resultados de la Rama Judicial se implementó mediante **XPath dinámico posicional**, apuntando directamente a la sexta fila (`tr`) del cuerpo de la tabla HTML:

```xpath
(//table[contains(@class,'tabla-resultados')]//tbody/tr)[6]/td[1]//a
```

**Por qué este enfoque:**
- El portal de la Rama Judicial no asigna IDs fijos ni atributos únicos a cada fila de resultados, por lo que un selector por atributo no es confiable.
- El uso de un índice posicional `[6]` en el XPath garantiza que siempre se apunta a la sexta fila contando desde arriba, independientemente del contenido de las otras filas.
- Antes de hacer clic, el bot ejecuta una **validación de conteo**: cuenta la cantidad de filas `<tr>` presentes en la tabla. Si el conteo es **menor a 6**, lanza una `Business_Exception` con código `BRE-02` ("Resultados insuficientes"), notifica por correo a `jhrey@tcc.com.co` y termina la transacción sin interrumpir el flujo general.

### 4.2 Cómo se extrae el nombre del correo

El nombre de la persona a consultar se extrae directamente del **cuerpo (Body) del correo electrónico** recibido en la bandeja de Gmail:

- El bot se conecta vía **IMAP** al correo configurado usando el módulo Gmail de Rocketbot con la credencial `Gmail_ConsultaJudicial`.
- Lee los correos no leídos y accede al contenido del campo `Body` de cada mensaje.
- Aplica una **expresión regular (RegEx)** para identificar y capturar el nombre de la persona natural en formato texto plano (ej. `Oscar Martinez Davila`).
- El valor extraído se almacena en la variable `strNombreConsultar`.
- Si el cuerpo del correo no contiene un nombre identificable o el formato es inválido, el bot lanza una `Business_Exception` con código `BRE-01`, registra el evento en el log de auditoría y continúa con el siguiente correo sin detener el proceso.

### 4.3 Cómo se maneja la descarga del archivo

La descarga del historial de actuaciones se gestiona con una **estrategia de espera inteligente** y verificación de archivo nuevo, en los siguientes pasos:

1. **Inventario previo:** Antes de iniciar la descarga, el bot registra la lista de archivos existentes en la carpeta `Downloads\` y guarda el timestamp del archivo más reciente.
2. **Trigger de descarga:** Se hace clic en el botón "Descargar DOC" dentro de la pantalla de detalle del proceso en la Rama Judicial.
3. **Espera inteligente:** En lugar de usar un `sleep` fijo, el bot entra en un bucle de verificación que compara continuamente la lista de archivos en `Downloads\` contra el inventario previo. El bucle se rompe únicamente cuando detecta **un nuevo archivo** o cuando alcanza el timeout definido (30 segundos).
4. **Identificación del archivo:** Una vez detectado el nuevo archivo (la descarga más reciente en la carpeta), se valida que su tamaño sea mayor a 0 KB para confirmar que la descarga fue exitosa y no resultó en un archivo corrupto.
5. **Registro:** La ruta absoluta del archivo y la URL de origen se almacenan en la tabla `B01_ConsultaJudicial_Transacciones` en los campos `strRutaDocumento` y `UrlWeb`.
6. **Reintento en fallo:** Si el archivo no aparece o pesa 0 KB, el bot elimina el temporal, refresca la página de detalle y reintenta la descarga hasta **2 veces** antes de marcar la transacción como `System_Exception`.

---

## 5. Limitaciones y trabajo pendiente

### 5.1 Qué no se alcanzó a implementar

| # | Funcionalidad | Detalle |
|---|---------------|---------|
| 1 | **Ejecución programada (Scheduled Trigger)** | El bot actualmente se ejecuta de forma manual desde Rocketbot Studio. No se configuró una tarea programada en el Programador de tareas de Windows para ejecuciones automáticas en horario de oficina (Lunes a Viernes, 8:00 a.m. - 5:00 p.m.). |
| 2 | **Soporte para múltiples correos en la misma ejecución** | El flujo actual está optimizado para procesar un correo por ejecución. La lógica para iterar sobre múltiples correos no leídos en una sola pasada no quedó completamente validada en la versión estable. |
| 3 | **Dashboard o reporte consolidado de métricas** | No se implementó un reporte visual (HTML o tabla en correo) con métricas de calidad mensual: volumen total procesado, % de tasa de éxito, AHT del bot vs. humano. Está definido en el PDD (Sección III.7) pero no se desarrolló en este alcance. |
| 4 | **Contenerización con Docker** | No aplica directamente a Rocketbot Studio, pero podría haberse explorado para aislar dependencias del entorno en otro enfoque. |
| 5 | **Movimiento de correos procesados a carpeta** | El PDD define que los correos con `BRE-01` (nombre inválido) deben moverse a una carpeta "No procesados" dentro de Gmail. Esta acción de carpeta no quedó completamente implementada. |

### 5.2 Qué se mejoraría con más tiempo

| # | Mejora | Justificación |
|---|--------|---------------|
| 1 | **Ejecución programada + trigger de correo en paralelo** | Configurar una tarea en el Programador de Windows que lance el bot cada N minutos en horario laboral, haciendo que el disparador sea verdaderamente desatendido sin intervención manual. |
| 2 | **Logging estructurado con niveles configurables** | Estandarizar el formato del log como JSON o CSV con campos fijos (`timestamp`, `level`, `hu`, `correlationId`, `message`) para facilitar la integración con herramientas de monitoreo o dashboards. |
| 3 | **Parametrización del intervalo de reintentos** | Actualmente los reintentos (máximo 3) están configurados como constante en el flujo. Moverlos a la tabla `Config` permitiría ajustar la resiliencia del bot sin modificar el código. |
| 4 | **Validación de CAPTCHA con alerta temprana** | Implementar una detección proactiva de CAPTCHA antes de intentar la búsqueda, para reducir el tiempo perdido en reintentos cuando el portal gubernamental activa este mecanismo de seguridad. |
| 5 | **Soporte multi-correo en una sola ejecución** | Refactorizar `HU01` y `HU02` para que iteren sobre todos los correos no leídos en la bandeja, procesando cada nombre como una transacción independiente dentro de la misma ejecución del bot. |
| 6 | **Renombrado descriptivo del archivo descargado** | Agregar la lógica de renombrado del CSV descargado con el formato `detalle_proceso_{nombre}_{fecha}.csv` antes de guardarlo, siguiendo la convención definida en los criterios de aceptación del reto. |
| 7 | **Pruebas unitarias por HU** | Crear casos de prueba documentados para cada Historia de Usuario que validen los escenarios de éxito, excepción de negocio y excepción de sistema por separado. |

---

## Manejo de Excepciones (resumen)

### Excepciones de Negocio (Business Exceptions)

| Código | Nombre | Condición | Acción del Bot |
|--------|--------|-----------|----------------|
| BRE-01 | Formato de correo inválido | `strNombreConsultar` = nulo o vacío | Registra en log, marca transacción como `Business_Exception`, notifica al remitente y continúa con el siguiente correo. |
| BRE-02 | Resultados insuficientes | Filas en tabla < 6 | Registra en log, cierra la búsqueda, envía correo a `jhrey@tcc.com.co` informando el caso y continúa. |
| BRE-03 | Sin archivo adjunto en registro #6 | Enlace de descarga ausente en UI | Toma captura de pantalla, adjunta al correo de alerta a `jhrey@tcc.com.co` y cierra el registro. |

### Excepciones de Sistema (System Exceptions)

| Código | Nombre | Condición | Acción del Bot |
|--------|--------|-----------|----------------|
| SYS-01 | Timeout / Error 500 Rama Judicial | Elemento UI no encontrado en 30 segundos | Cierra Chrome, espera 10 segundos, reintenta hasta 3 veces. Si falla definitivamente, notifica por correo y adjunta screenshot. |
| SYS-02 | Fallo de conexión al servidor de correo | IMAP/SMTP timeout o `Connection Refused` | Reintento lógico 3 veces. Si falla, detiene la ejecución general. |
| SYS-03 | Descarga interrumpida o archivo corrupto | Archivo en `Downloads\` pesa 0 KB | Elimina temporal, refresca la página de detalle, reintenta descarga hasta 2 veces. |
| SYS-XX | Excepción desconocida | Cualquier error no clasificado | Suspende la transacción, adjunta screenshot (`/screenshots/system_error.png`) y log de traza al correo de alerta a `jhrey@tcc.com.co`. |

> **Nota sobre CAPTCHA:** Si el portal de la Rama Judicial activa un CAPTCHA, el bot lo reporta como `System_Exception` no recuperable, ya que está fuera del alcance de la automatización resolver bloqueos de este tipo según el PDD.

---

## Información del proyecto

| Campo | Detalle |
|-------|---------|
| **Candidato** | Jonathan Rincón |
| **Herramienta** | Rocketbot Studio 2025 |
| **Evaluador** | Jairo Humberto Rey Castro — `jhrey@tcc.com.co` |
| **Organización** | TCC - Tecnología, Consultoría y Capacitación |
| **Departamento** | Desarrollo Integral de Aplicaciones (DIA) |
| **Versión estable** | Preview v2.0 |