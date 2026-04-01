FROM node:20-alpine AS builder

# Set the working directory for the build process (This is where files will land)
WORKDIR /app

# Copy dependency files relative to the Dockerfile's location
# The build context is the folder containing these files.
COPY package.json package-lock.json ./

# Install dependencies (Slowest step, protected by caching)
RUN npm install

# Copy all source files (The rest of the project: src/, public/, etc.)
COPY . .

# Run the React build command. Output goes to /app/dist
RUN npm run build

# ==============================
# 2. RUNNER STAGE: Serving the Static Assets
# ==============================
FROM nginx:alpine

# Copy the built static assets from the 'builder' stage
# The path in the builder stage is now simply /app/dist
COPY --from=builder /app/dist /usr/share/nginx/html

# This overwrites the default Nginx config
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expose and Run
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
