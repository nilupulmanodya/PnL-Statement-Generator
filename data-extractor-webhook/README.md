# Flask Webhook Server Setup

This guide explains how to set up the Flask server for handling webhooks from Supabase in the **Quarterly P&L Extraction from CSE Reports** project.

## Prerequisites

Before setting up the Flask server, ensure you have the following:
- Python **3.8+** installed.
- A virtual environment (optional but recommended).
- Required dependencies installed.

## Step 1: Clone the Repository

```sh
git clone <https://github.com/nilupulmanodya/PnL-Statement-Generator.git>
cd <your-project-directory>
```

## Step 2: Create a Virtual Environment (Optional)

It is recommended to use a virtual environment to manage dependencies.

```sh
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

## Step 3: Install Dependencies

Run the following command to install required Python packages:

```sh
pip install -r requirements.txt
```


## Step 4: Configure Environment Variables

Create a `.env` file in the root directory with the following content:

```env
OPENAI_API_KEY=your-openai-api-key
SUPABASE_URL=your-supabase-url
SUPABASE_KEY=your-supabase-anon-key
BUCKET_NAME=your-storage-bucket-name

```

## Step 5: Start the Flask Server

Run the Flask server:
```sh
python webhook_listner.py
```

## Step 6: Verify Webhook Endpoint

Your Flask server listens for incoming Supabase webhook requests at:

```
http://<your-server-ip>:5000/webhook
```

Use `curl` or Postman to test:
```sh
curl -X POST http://127.0.0.1:5000/webhook -H "Content-Type: application/json" -d '{"test": "data"}'
```

## Step 7: Deploying the Flask Server

To deploy the Flask server, you can use:
- **Docker** (recommended)
- **Gunicorn + Nginx**
- **Cloud providers** (e.g., AWS, Heroku, Railway.app)
