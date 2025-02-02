# Frontend Setup (Vite + React)

This guide provides instructions to set up and run the **Vite frontend** for the **Quarterly P&L Extraction from CSE Reports** project.

## Prerequisites

Before setting up the frontend, ensure you have the following:
- **Node.js** (version 16+ recommended)
- **npm** or **yarn** installed
- A configured **Supabase backend**

## Step 1: Clone the Repository

```sh
git clone <https://github.com/nilupulmanodya/PnL-Statement-Generator.git>
cd <your-project-directory>/frontend
```

## Step 2: Install Dependencies

Run the following command to install project dependencies:

```sh
npm install  # or yarn install
```

## Step 3: Configure Environment Variables

Create a `.env` file in the root of the frontend directory with the following content:

```env
VITE_SUPABASE_URL=<your-supabase-url>
VITE_SUPABASE_ANON_KEY=<your-anon-key>

```
## Step 4: Run the Development Server

To start the development server, run:

```sh
npm run dev  # or yarn dev
```

By default, the app will be available at:
```
http://localhost:5173
```

## Step 5: Building for Production

To generate a production build:

```sh
npm run build  # or yarn build
```

The output will be stored in the `dist/` folder.

## Step 6: Deploying the Frontend

To deploy the frontend, you can use:
- **Vercel**
- **Netlify**
- **Cloudflare Pages**
- **AWS S3 + CloudFront**
