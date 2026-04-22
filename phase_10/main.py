from webapp import create_app


app = create_app()


if __name__ == "__main__":
    # Port 5001 avoids macOS AirPlay Receiver binding to 5000 (often returns HTTP 403).
    app.run(debug=True, host="127.0.0.1", port=5001)
