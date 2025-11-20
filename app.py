from src.dashboard import app as dash_app

# Expose the WSGI callable for Gunicorn
app = dash_app.server

if __name__ == "__main__":
    # Dash 3.x uses `run` instead of the older `run_server` API
    dash_app.run(host="0.0.0.0", port=8050, debug=False)
