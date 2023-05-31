FROM nginx:latest

COPY nginx.conf /etc/nginx/nginx.conf

# Start Nginx
CMD ["nginx", "-g", "daemon off;", "-c", "/etc/nginx/nginx.conf"]