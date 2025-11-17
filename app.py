from src.dashboard import app as dash_app

# Expose the WSGI callable for Gunicorn
app = dash_app.server

if __name__ == "__main__":
    dash_app.run_server(host="0.0.0.0", port=8050, debug=False)
