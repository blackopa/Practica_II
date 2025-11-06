# Evaluador Automatizado de Informes (EVA)

EVA es una aplicación web desarrollada con Django que automatiza la revisión y procesamiento de informes en formato PDF. Esta herramienta está diseñada para analizar y validar documentos PDF según criterios específicos, generando reportes detallados de su contenido.

## 🚀 Características Principales

- Procesamiento automatizado de documentos PDF
- Interfaz web intuitiva para la carga y revisión de documentos
- Generación de reportes detallados
- Sistema de seguimiento por RUT y nombre de persona
- Almacenamiento y gestión de informes históricos
- Validación automática del contenido según criterios predefinidos

## 📁 Estructura del Proyecto

```
├── mainapp/                  # Aplicación principal
│   ├── validations/         # Módulos de validación
│   │   ├── process_file.py  # Procesamiento de archivos
│   │   └── Informe_datos.py # Análisis de datos
│   ├── views.py             # Vistas de la aplicación
│   └── models.py            # Modelos de datos
├── templates/               # Plantillas HTML
├── static/                 # Archivos estáticos (CSS, JS)
└── pdfreviewproject/       # Configuración del proyecto Django
```

## 🔧 Requisitos Previos

1. Docker Desktop
   - Descargar e instalar desde: https://www.docker.com/products/docker-desktop/
   - Reiniciar el sistema después de la instalación

## 🚀 Instalación y Ejecución

1. Clonar el repositorio:
```bash
git clone https://github.com/Mineduc-CentroInnovacion/Eva.git
cd Eva
```

2. Ejecutar el script de construcción:
```bash
build.bat
```

Este script realizará las siguientes acciones:
- Creará los directorios necesarios para los datos y archivos temporales
- Construirá la imagen Docker del proyecto
- Iniciará el contenedor con la aplicación

## 💻 Uso

1. Una vez que el contenedor esté en ejecución, acceder a:
   - http://localhost:80

2. En la interfaz web:
   - Ingresar el RUT y nombre de la persona
   - Cargar el archivo PDF a analizar
   - Especificar las páginas a procesar
   - Enviar el formulario para obtener el reporte

## 🛠️ Tecnologías Utilizadas

- Python/Django - Framework web
- Docker - Containerización
- Bootstrap - Framework CSS
- PostgreSQL - Base de datos (configurado pero comentado en build.bat)

## � Estructura del PDF

La aplicación está configurada para procesar PDFs con una estructura específica. La configuración de las ubicaciones de los elementos se encuentra en la clase `DatosTextoInforme` dentro de `mainapp/validations/Informe_datos.py`. Las secciones principales incluyen:

- **Actividad Asesoría**: Primeros 9 elementos del informe
- **Elementos de Red**: Elementos 12-18
- **Tramos de Canalización**: Elementos 25-46
- **Cables**: Elementos 49-53
- **Enlaces Existentes**: A partir del elemento 56
- **Racks Existentes**: Ubicación dinámica después de Enlaces Existentes
- **Racks Proyectados**: Ubicación dinámica después de Racks Existentes
- **Puntos Proyectados**: Ubicación dinámica después de Racks Proyectados
- **Tramos Proyectados**: Ubicación dinámica después de Puntos Proyectados

Las tablas con tamaño variable se manejan mediante la función `tablas_rango_variable()` que determina dinámicamente el final de cada sección.

## �📝 Notas Importantes

- La aplicación está configurada para procesar documentos PDF con el formato específico descrito arriba
- Los archivos temporales se almacenan en `static/tmp/`
- Los datos persistentes se almacenan en el directorio `data/`
- Modificar las ubicaciones de los elementos requiere actualizar la configuración en `Informe_datos.py`
