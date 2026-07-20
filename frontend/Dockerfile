# Build stage
FROM node:20-alpine AS builder

WORKDIR /app/frontend

COPY frontend/package*.json ./

RUN npm install

COPY frontend/ .

RUN npm run build

# Production stage
FROM node:20-alpine

WORKDIR /app

# Install serve to run the SPA
RUN npm install -g serve

# Copy built app from builder
COPY --from=builder /app/frontend/dist ./dist

EXPOSE 5173

# Set environment for frontend
ENV VITE_API_URL=http://qresolve-api:8000/api/v1

CMD ["serve", "-s", "dist", "-l", "5173"]
