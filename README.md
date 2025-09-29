# Mi Servidor Python para Android + FCM + PHP

Este servidor:
- Recibe peticiones de tu app Android
- Se conecta a tu API PHP para leer/escribir en la DB
- Envía notificaciones push con Firebase FCM

## Endpoints
- GET `/test-api` → Prueba conexión con PHP
- POST `/send-notification` → Envía noti a un dispositivo
- GET `/get-data` → Obtiene datos de la DB
