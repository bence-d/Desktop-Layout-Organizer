FROM nginx:alpine
COPY ./dist/angular-webserver ./usr/share/nginx/html
<<<<<<< Updated upstream
COPY ./nginx-custom.conf /etc/nginx/conf.d/default.conf
=======
RUN npm install -g @angular/cli
CMD ["ng", "serve", "--host", "0.0.0.0"]
>>>>>>> Stashed changes
