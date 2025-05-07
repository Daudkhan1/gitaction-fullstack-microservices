# frontend/Dockerfile

FROM nginx:alpine

# Copy custom index.html to the default nginx html directory
COPY index.html /usr/share/nginx/html/index.html

# Expose port 80 for the container
EXPOSE 80

# Start nginx
CMD ["nginx", "-g", "daemon off;"]
