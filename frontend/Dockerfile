FROM denoland/deno:2.0.0 as build
WORKDIR /app

# Copy source
COPY . .

# Build with Deno tasks (Vite build)
RUN deno task build

FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
COPY <<EOF /etc/nginx/conf.d/default.conf
server {
  listen 80;
  server_name _;
  root /usr/share/nginx/html;
  index index.html;
  location / {
    try_files $uri /index.html;
  }
}
EOF


