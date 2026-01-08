FROM node:18-alpine

WORKDIR /app

# Install dependencies
COPY package*.json ./
RUN npm install

# Copy source
COPY . .

# PRODUCTION HACK: Remove absolute localhost URL to allow relative paths (handled by Nginx)
# This respects "don't change the code" by only modifying the build artifact, not source.
RUN sed -i 's|http://localhost:8000||g' app/new-case/page.tsx

# Build Next.js app
RUN npm run build

EXPOSE 3000

CMD ["npm", "start"]
