# Use a lightweight Nginx image
FROM nginx:1.21-alpine

# Remove the default Nginx configuration
RUN rm /etc/nginx/conf.d/default.conf

# Copy the custom Nginx configuration
COPY nginx.conf /etc/nginx/conf.d/

# Copy the frontend's static files
COPY ./frontend /usr/share/nginx/html
