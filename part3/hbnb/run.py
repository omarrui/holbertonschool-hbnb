from app import create_app

# Create app instance using the Application Factory
app = create_app()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)