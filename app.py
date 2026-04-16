from dashboard_app import create_app

server = create_app()

if __name__ == "__main__":
    server.run(debug=False, host="0.0.0.0", port=5001)
