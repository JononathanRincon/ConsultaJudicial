CREATE TABLE IF NOT EXISTS B01_ConsultaJudicial_Config (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    Name        TEXT NOT NULL UNIQUE,
    Prod        TEXT,
    Dev         TEXT,
    Description TEXT
);

-- Registros iniciales obligatorios
INSERT INTO B01_ConsultaJudicial_Config (Name, Prod, Dev, Description) VALUES 
('Produccion', 'False', 'True', 'Define el ambiente activo para lectura de variables'),
('UrlRamaJudicial', 'https://consultaprocesos.ramajudicial.gov.co/Procesos/NombreRazonSocial', 'https://consultaprocesos.ramajudicial.gov.co/Procesos/NombreRazonSocial', 'URL del portal de la Rama Judicial'),
('EmailResponsable', 'jhrey@tcc.com.co', 'Jonathanandres080@gmail.com', 'Destinatario de notificaciones y documentos'),
('PathLogs', 'C:\RPA_Rocketbot\Logs\', 'C:\RPA_Rocketbot\Logs\', 'Ruta base para almacenamiento de logs diarios');


CREATE TABLE IF NOT EXISTS B01_ConsultaJudicial_Flags (
    hu              INTEGER PRIMARY KEY,
    taskname        TEXT NOT NULL,
    attempts        INTEGER DEFAULT 0,
    finished        TEXT DEFAULT 'False',
    date            TEXT NOT NULL -- Formato YYYY-MM-DD
);

-- Inicialización del flujo transaccional
INSERT INTO B01_ConsultaJudicial_Flags (hu, taskname, attempts, finished, date) VALUES 
(1, 'HU01_Recepcion_Solicitudes', 0, 'False', date('now')),
(2, 'HU02_Busqueda_RamaJudicial', 0, 'False', date('now')),
(3, 'HU03_Descarga_Expediente', 0, 'False', date('now')),
(4, 'HU04_Notificacion_Cierre', 0, 'False', date('now'));


CREATE TABLE IF NOT EXISTS B01_ConsultaJudicial_Transacciones (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    strNombreConsultar  TEXT NOT NULL,
    strRadicado         TEXT,
    strRutaDocumento    TEXT,
    Status              TEXT DEFAULT 'Pending', -- Pending, Processed, Business_Exception, System_Exception
    ProcessDate         TEXT,                   -- Formato YYYY-MM-DD HH:mm:ss
    Notes               TEXT,                   -- Detalle de errores o hitos
    CorrelationId       TEXT                    -- ID único de ejecución para trazabilidad [cite: 633]
);