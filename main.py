from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# === CONFIGURACIÓN ===
# 🔥 Reemplaza esto con tu clave de servidor de Firebase
FIREBASE_SERVER_KEY = "AAAA...tu_clave_aqui"

# Tu API PHP en RunHosting
API_PHP_URL = "http://pruebaproyecto1.atwebpages.com/test_conn.php"
FCM_URL = "https://fcm.googleapis.com/fcm/send"

# === ruta principal ===
@app.route('/')
def home():
    return '''
    <h2>🚀 Servidor Python en Render</h2>
    <p><a href="/test-api">✅ Probar conexión con tu API PHP</a></p>
    <p><a href="/get-data">🔁 Obtener datos de la base de datos</a></p>
    <small>Tu backend para Android + FCM + PHP está funcionando.</small>
    '''

# === RUTA: Probar conexión con tu API PHP ===
@app.route('/test-api')
def test_api():
    try:
        response = requests.get(
            API_PHP_URL,
            params={'test': 'python-server', 'from': 'android-backend'},
            timeout=10
        )
        return jsonify({
            'status': 'success',
            'message': 'Conexión con API PHP exitosa',
            'data': response.json() if response.ok else response.text
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

#---------------------------------------------------------------------------------
# === RUTA: Enviar notificación push via FCM ===
@app.route('/send-notification', methods=['POST'])
def send_notification():
    data = request.json
    token = data.get('token')
    title = data.get('title', 'Notificación')
    body = data.get('body', 'Hola desde tu servidor!')

    if not token:
        return jsonify({'error': 'Falta el token FCM'}), 400

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'key={FIREBASE_SERVER_KEY}'
    }

    payload = {
        'to': token,
        'notification': {
            'title': title,
            'body': body
        },
        'data': {
            'click_action': 'FLUTTER_NOTIFICATION_CLICK'
        }
    }

    try:
        resp = requests.post(FCM_URL, json=payload, headers=headers, timeout=10)
        if resp.status_code == 200:
            return jsonify({'status': 'sent', 'response': resp.json()})
        else:
            return jsonify({'error': f'FCM Error {resp.status_code}', 'details': resp.text}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

#------------------------------------------------------------------------
# === RUTA: Obtener datos de la DB (vía API PHP) ===
@app.route('/get-data')
def get_data():
    try:
        # Aquí llamas a tu API PHP para obtener datos de la DB
        response = requests.get(API_PHP_URL, timeout=10)
        return jsonify({
            'from_php': response.json() if response.ok else 'Error'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Iniciar servidor
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
