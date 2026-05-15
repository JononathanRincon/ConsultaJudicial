# coding: utf-8
correoInicio = r"""<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>Notificación Bot {NombreBot}</title>
  <style>
   
    .container {{
      width: 650px;
      margin: 20px auto;
      border: 1px solid #dddddd;
      font-family: Arial, sans-serif;
      font-size: 14px;
      color: #333333;
      box-shadow: 0 2px 6px rgba(0,0,0,0.1);
    }}
    
    .header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 10px 20px;
      border-bottom: 4px solid #4CAF50;
      box-shadow: 0 2px 4px rgba(0,0,0,0.1);
      background: #f9fff9;
    }}
    .header img {{
      max-height: 80px;
      display: block;
    }}
    /* Cuerpo del mensaje */
    .content {{
      padding: 20px;
      text-align: start;
      line-height: 1.5;
    }}
    .content h2 {{
      text-align: center;
      color: #4CAF50;
      margin-top: 0;
    }}
    .content ul {{
      margin: 10px 0 20px 20px;
    }}
    .content ul li {{
      margin-bottom: 8px;
    }}
    
    .footer {{
      padding: 10px;
      text-align: center;
      font-size: 12px;
      color: #777777;
      border-top: 1px solid #eeeeee;
      background: #f9f9f9;
    }}
    .content ul {{
    margin: 0;         
  }}
  .content ul li {{
    margin: 0px 0px;    
    padding: 0px;
  }}
  </style>
</head>
<body>
  <table class="container" cellpadding="0" cellspacing="0">
        <tr>
            <td style="padding: 10px 20px; background: #f9fff9; border-bottom: 4px solid #4CAF50;">
              <table width="100%" cellpadding="0" cellspacing="0" border="0">
                <tr>
                  <td align="left" valign="middle" style="width:50%; padding:10px 0;">
                    <img src="cid:logoFCV" alt="Logo FCV" style="max-height:70px; display:block;">
                  </td>
                  <td align="right" valign="middle" style="width:50%; padding:10px 0;">
                      <!-- vacío -->
                  </td>
                </tr>
              </table>                
            </td>
        </tr>
    
    <tr>
      <td class="content">
        <!-- Título centrado -->
        <h2>Inicio de ejecución Bot {NombreBot}</h2>
        <!-- Mensaje justificado -->
        <p>Estimado(s),<br><br>
        Se notifica el <strong>inicio</strong> del proceso automatizado de <strong>{NombreBot}</strong>.
        </p>

        <ul>
        <li><strong>Fecha/Hora de inicio:</strong> {FechaInicio}</li>
        <li><strong>Ambiente:</strong> {Ambiente}</li>
        <li><strong>Ruta de log:</strong> {RutaLog}</li>
        </ul>

        <p>
        Una vez finalizado, recibirá un resumen detallado de los resultados.<br><br>
        Cordialmente,<br>
        Asistente <strong>{NombreBot}</strong>.
        </p>

      </td>
    </tr>
    <tr>
      <td class="footer">
        © {Ano} Fundación Cardiovascular de Colombia
      </td>
    </tr>
  </table>
</body>
</html>"""

MensajeFin = r"""<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>Notificación de Finalización - {NombreBot}</title>
  <style>
    .container {{
      width: 650px;
      margin: 20px auto;
      border: 1px solid #dddddd;
      font-family: Arial, sans-serif;
      font-size: 14px;
      color: #333333;
      box-shadow: 0 2px 6px rgba(0,0,0,0.1);
    }}
    .header {{
      padding: 10px 20px;
      border-bottom: 4px solid #1565C0; /* Azul */
      box-shadow: 0 2px 4px rgba(0,0,0,0.1);
      background: #f2f9ff;
    }}
    .header img {{
      max-height: 70px;
      display: block;
    }}
    .content {{
      padding: 20px;
      text-align: justify;
      line-height: 1.5;
    }}
    .content h2 {{
      text-align: center;
      color: #1565C0;
      margin-top: 0;
    }}
    .content ul {{
      margin: 10px 0 20px 0;
      padding-left: 30px;
    }}
    .content ul li {{
      margin: 0;
      padding: 0;
      line-height: 1.4;
    }}
    .footer {{
      padding: 10px;
      text-align: center;
      font-size: 12px;
      color: #777777;
      border-top: 1px solid #eeeeee;
      background: #f9f9f9;
    }}
    .header img.logo-fcv {{
      max-height: 70px;
      float: left;
    }}
  </style>
</head>
<body>
  <table class="container" cellpadding="0" cellspacing="0">
    <tr>
      <td class="header">
            <table width="100%" cellpadding="0" cellspacing="0" border="0">
                <tr>
                  <td align="left" valign="middle" style="width:50%; padding:10px 0;">
                    <img src="cid:logoFCV" alt="Logo FCV" style="max-height:70px; display:block;">
                  </td>
                  <td align="right" valign="middle" style="width:50%; padding:10px 0;">
                      <!-- vacío -->
                  </td>
                </tr>
              </table>
        </td>
    </tr>
    <tr>
      <td class="content">
        <h2>Finalización de ejecución Bot {NombreBot}</h2>
        <p>
          Estimado(s),<br><br>
          El proceso automatizado <strong>{NombreBot}</strong> ha finalizado su ejecución.
        </p>
        <ul>
          <li><strong>Hora de finalización:</strong> {FechaFin}</li>
          <li><strong>Registros procesados:</strong> {TotalProcesados}</li>
          <li><strong>Ruta de log:</strong> {RutaLog}</li>
        </ul>
        <p>
          Si requiere mayor detalle, puede consultar el log adjunto o contactar a soporte.<br><br>
          Cordialmente,<br>
          Asistente <strong>{NombreBot}</strong>.
        </p>
      </td>
    </tr>
    <tr>
            <td class="footer">
                © {Ano} Fundación Cardiovascular de Colombia
            </td>
        </tr>
  </table>
</body>
</html>
"""

MensajeEnvioNotificacion =r"""<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>Resumen Bot {NombreBot}</title>
  <style>
    .container {{
      width: 650px;
      margin: 20px auto;
      border: 1px solid #dddddd;
      font-family: Arial, sans-serif;
      font-size: 14px;
      color: #333333;
      box-shadow: 0 2px 6px rgba(0,0,0,0.1);
    }}
    .header {{
      padding: 10px 20px;
      border-bottom: 4px solid #455A64; /* Gris oscuro */
      box-shadow: 0 2px 4px rgba(0,0,0,0.1);
      background: #f4f7f9;
    }}
    .header img {{
      max-height: 70px;
      display: block;
    }}
    .content {{
      padding: 20px;
      text-align: justify;
      line-height: 1.5;
    }}
    .content h2 {{
      text-align: center;
      color: #455A64;
      margin-top: 0;
    }}
    .content ul {{
      margin: 10px 0 20px 0;
      padding-left: 20px;
    }}
    .content ul li {{
      margin: 0;
      padding: 0;
      line-height: 1.4;
    }}
    .footer {{
      padding: 10px;
      text-align: center;
      font-size: 12px;
      color: #777777;
      border-top: 1px solid #eeeeee;
      background: #f9f9f9;
    }}
    .header img.logo-fcv {{
      max-height: 70px;
      float: left;
    }}
  </style>
</head>
<body>
  <table class="container" cellpadding="0" cellspacing="0">
    <tr>
      <td class="header">
        <table width="100%" cellpadding="0" cellspacing="0" border="0">
                <tr>
                  <td align="left" valign="middle" style="width:50%; padding:10px 0;">
                    <img src="cid:logoFCV" alt="Logo FCV" style="max-height:70px; display:block;">
                  </td>
                  <td align="right" valign="middle" style="width:50%; padding:10px 0;">
                      <!-- vacío -->
                  </td>
                </tr>
              </table>
      </td>
    </tr>
    <tr>
      <td class="content">
        <h2>Resumen de ejecución Bot {NombreBot}</h2>
        <p>
          Estimado(s),<br><br>
          {MensajeEnvio}
        <p>
          Para mayor detalle, puede consultar el archivo adjunto o comunicarse con soporte.<br><br>
          Cordialmente,<br>
          Asistente <strong>{NombreBot}</strong>.
        </p>
      </td>
    </tr>
    <tr>
      <td class="footer">
        © {Ano} Fundación Cardiovascular de Colombia
      </td>
    </tr>
  </table>
</body>
</html>
"""
NotificacionError = r"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Novedad en ejecución Bot - {NombreBot}</title>
    <style>
        .container {{
            width: 650px;
            margin: 20px auto;
            border: 1px solid #dddddd;
            font-family: Arial, sans-serif;
            font-size: 14px;
            color: #333333;
            box-shadow: 0 2px 6px rgba(0,0,0,0.1); /* Sombra general para el contenedor */
        }}
        .header {{
            padding: 10px 20px;
            border-bottom: 4px solid #FF5722;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            background: #FFF3E0; 
        }}
        .header img {{
            max-height: 70px; /* Ajusta el tamaño máximo para ambos logos */
            display: block;
        }}
        .header .logo-fcv {{
            max-height: 70px; /* FCV es un poco más grande */
        }}
        .content {{
            padding: 20px;
            text-align: justify;
            line-height: 1.5;
        }}
        .content h2 {{
            text-align: center;
            color: #FF5722;
            margin-top: 0;
        }}
        .content ul {{
            margin: 10px 0 20px 0;
            padding-left: 20px;
        }}
        .content ul li {{
            margin: 0;
            padding: 0;
            line-height: 1.4;
        }}
        .footer {{
            padding: 10px;
            text-align: center;
            font-size: 12px;
            color: #777777;
            border-top: 1px solid #eeeeee;
            background: #f9f9f9;
        }}    
    </style>
</head>
<body>
    <table class="container" cellpadding="0" cellspacing="0">
        <tr>
            <td class="header">
                <table width="100%" cellpadding="0" cellspacing="0" border="0">
                <tr>
                  <td align="left" valign="middle" style="width:50%; padding:10px 0;">
                    <img src="cid:logoFCV" alt="Logo FCV" style="max-height:70px; display:block;">
                  </td>
                  <td align="right" valign="middle" style="width:50%; padding:10px 0;">
                      <!-- vacío -->
                  </td>
                </tr>
              </table>
            </td>
        </tr>
        <tr>
            <td class="content">
                <h2>Novedad en ejecución Bot {NombreBot}</h2>
                <div>
                    <p>
                        Estimado(s),<br><br>
                        Se ha presentado una <b>Novedad</b> en la ejecución del bot <b>{NombreBot}</b>.
                    </p>
                    <ul>
                        <li><b>Fecha del Evento:</b> {FechaEvento}</li>
                        <li><b>Ambiente:</b> {Ambiente}</li>
                        <li><b>Tipo de Alerta:</b> {TipoAlerta}</li>
                        <li><b>Descripcion de la Alerta:</b> {DescripcionAlerta}</li>
                        <li><b>Ruta Log:</b> {RutaLog}</li>
                    </ul>
                    <p>
                        Por favor, revisa el log para más detalles.<br><br>
                        Cordialmente,<br>
                        Asistente <strong>{NombreBot}</strong>.
                    </p>
                </div>
            </td>
        </tr>
        <tr>
            <td class="footer">
                © {Ano} Fundación Cardiovascular de Colombia
            </td>
        </tr>
    </table>
</body>
</html>"""