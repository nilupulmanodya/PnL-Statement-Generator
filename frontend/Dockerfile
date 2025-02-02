# Use Node.js to build the frontend
FROM node:18 AS build

# Set working directory
WORKDIR /app

# Copy package.json and package-lock.json (for npm)
COPY package.json package-lock.json ./ 

# Install dependencies using npm
RUN npm install --frozen-lockfile

# Copy the rest of the app source
COPY . . 

# Build the project
RUN npm run build

# Use Nginx to serve the frontend
FROM nginx:alpine

# Copy the custom Nginx config
COPY default.conf /etc/nginx/conf.d/default.conf

# Copy the built frontend files from the previous stage
COPY --from=build /app/dist /usr/share/nginx/html

# Expose port
EXPOSE 80

# Start Nginx
CMD ["nginx", "-g", "daemon off;"]
