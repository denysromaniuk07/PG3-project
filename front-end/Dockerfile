# Stage 1: Build
FROM node:18-alpine as builder

# Set working directory
WORKDIR /app

# Copy package files
COPY package*.json ./
COPY tsconfig*.json ./
COPY tailwind.config.js ./
COPY postcss.config.js ./

# Install dependencies
RUN npm ci

# Copy source code
COPY public ./public
COPY src ./src
COPY AI-Career ./AI-Career

# Build application
RUN npm run build


# Stage 2: Production Runtime
FROM node:18-alpine

# Install serve to run the application
RUN npm install -g serve

# Set working directory
WORKDIR /app

# Create non-root user
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nextjs -u 1001

# Copy built application from builder
COPY --from=builder --chown=nextjs:nodejs /app/build ./build
COPY --from=builder --chown=nextjs:nodejs /app/node_modules ./node_modules
COPY --from=builder --chown=nextjs:nodejs /app/package*.json ./

# Switch to non-root user
USER nextjs

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://localhost:3000 || exit 1

# Expose port
EXPOSE 3000

# Start application
CMD ["serve", "-s", "build", "-l", "3000"]
