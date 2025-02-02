# Supabase Setup and Configuration

This guide provides step-by-step instructions to set up Supabase for the **Quarterly P&L Extraction from CSE Reports** project. It covers configuring **Row-Level Security (RLS)**, enabling **webhooks**, and defining the necessary **trigger function** for automated processing.

## Prerequisites

Before setting up Supabase, ensure you have the following:
- A [Supabase](https://supabase.com/) account.
- A Supabase project created.
- `supabase-cli` installed (optional but recommended):
  ```sh
  npm install -g supabase
  ```
- A configured Supabase database with the required tables and storage buckets.

## Step 1: Set Row-Level Security (RLS) to Public

By default, Supabase applies strict security policies to tables and storage. For this project, we need to **disable RLS** for both storage and tables to allow public access.

### Disable RLS for the Table

1. Navigate to **Supabase Dashboard** → **Database** → **Tables**.
2. Select the relevant table (e.g., `public.table`).
3. Go to the **Security** tab.
4. Toggle **Enable Row-Level Security (RLS)** **OFF**.

Alternatively, if you prefer using SQL, execute:
```sql
ALTER TABLE public.table DISABLE ROW LEVEL SECURITY;
```

### Disable RLS for Storage

1. Navigate to **Supabase Dashboard** → **Storage** → **Buckets**.
2. Select the relevant storage bucket.
3. Ensure **Public Access** is enabled.

## Step 2: Enable Webhooks

Supabase supports webhooks that trigger functions upon specific table events. We will configure a webhook to trigger an external **Flask server** whenever a new record is inserted into our table.

1. Navigate to **Supabase Dashboard** → **Database** → **Triggers**.
2. Click **New Trigger** and configure:
   - **Name**: `my_webhook`
   - **Table**: `public.table`
   - **Event**: `AFTER INSERT`
   - **Function**: `supabase_functions.http_request`

3. Alternatively, execute the following SQL query:

```sql
CREATE TRIGGER "my_webhook"
AFTER INSERT ON "public"."table"
FOR EACH ROW
EXECUTE FUNCTION "supabase_functions"."http_request"(
  'https://python-webhook.app/webhook',  -- Webhook URL
  'POST',  -- HTTP Method
  '{"Content-Type":"application/json"}',  -- Headers
  '{}',  -- Request Body (empty)
  '1000'  -- Timeout in ms
);
```

## Step 3: Verify the Webhook

Once the trigger is created, test it by inserting a sample record into the table:

```sql
INSERT INTO public.table (column1, column2) VALUES ('test_value1', 'test_value2');
```

Check if your Flask server logs the incoming request. If the webhook fails, inspect **Supabase Logs** for errors.

## Step 4: Environment Variables

Ensure your backend services have access to the correct **Supabase environment variables**:

```sh
SUPABASE_URL=<your-supabase-url>
SUPABASE_ANON_KEY=<your-anon-key>
```

These variables are necessary to interact with Supabase programmatically.

## Conclusion

With these configurations, Supabase is now set up to:
- Allow public access to the required table and storage.
- Automatically trigger a webhook upon data insertion.
- Forward the data to the **Flask server** for further processing.

Ensure the **Flask webhook endpoint** is correctly set up to handle incoming data and process the quarterly P&L statements accordingly.

For any issues, refer to Supabase documentation: [https://supabase.com/docs](https://supabase.com/docs).