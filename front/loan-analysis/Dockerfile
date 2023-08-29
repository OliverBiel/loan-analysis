FROM node:16.14 as angular

WORKDIR /app
RUN npm install -g @angular/cli
RUN npm install --save-dev @angular-devkit/build-angular
COPY . /app
RUN npm install
RUN ng build -c production


FROM nginx:latest
COPY --from=angular /app/dist/loan-analysis /usr/share/nginx/html
EXPOSE 80
