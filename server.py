from app import create_app
import os

app = create_app()

if __name__ == '__main__':
    proDir = os.path.dirname(os.path.realpath(__file__))
    pemPath = os.path.join(proDir, "app\\3660880_www.younglass.com.pem")
    print(pemPath)
    keyPath = os.path.join(proDir, "app\\3660880_www.younglass.com.key")
    print(keyPath)
    app.run(debug=True, ssl_context=(pemPath, keyPath))