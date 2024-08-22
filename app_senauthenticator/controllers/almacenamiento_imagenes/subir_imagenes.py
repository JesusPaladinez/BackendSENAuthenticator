import pyrebase

config = {
  "apiKey": "AIzaSyAq7WwHvbgox2xJQHqK9yPYfrK3gpPt4K4",
  "authDomain": "projectstoragesenauthenticator.firebaseapp.com",
  "projectId": "projectstoragesenauthenticator",
  "storageBucket": "projectstoragesenauthenticator.appspot.com",
  "messagingSenderId": "371522976959",
  "appId": "1:371522976959:web:f99bc5b20a440aaac5da0a",
  "measurementId": "G-5TEEM4Y3P3",
  "service_account": "clave_cuenta_servicio.json",
  "databaseURL":"https://projectstoragesenauthenticator-default-rtdb.firebaseio.com/"
}

firebase_storage = pyrebase.initialize_app(config)
storage = firebase_storage.storage()

# Subir archivos
storage.child("objetos/amazon.jpeg").put("app_senauthenticator/controllers/almacenamiento_imagenes/amazon.jpeg")

