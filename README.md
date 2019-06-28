# TemperaturaSite
A little device to get informed about the temperature of my company's site

## Componentes

### TemperaturaSite.py
Se encarga de leer los datos provenientes del puerto serial cada segundo. Cada 3600 lecturas (1 hora) envia los datos leídos a una URL de Microsoft Flow que se encarga de introducir los datos en una lista de Sharepoint

### Flow.png
Ilustración de la configuración del flujo en Microsoft Flow
