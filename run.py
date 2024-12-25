from app import create_app
import os

app = create_app()

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # Ensure the correct port is read
    app.run(debug=True, port=port)  # Binding to 0.0.0.0 for Docker access

