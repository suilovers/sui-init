# Flask Application

This is a basic Flask application. You can run it either locally or inside a Docker container.

## Local Setup

Follow these steps to run the application locally:

1. Install the required Python packages:

    ```bash
    pip install -r requirements.txt
    ```

2. Run the application:

    ```bash
    ENV=development flask run -p 7777 --host 0.0.0.0
    ```

The application will be available at `http://localhost:7777`.