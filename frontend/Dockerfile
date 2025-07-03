FROM node:22.1.0

WORKDIR /app
COPY frontend/package.json frontend/yarn.lock ./
RUN yarn install
COPY frontend .
EXPOSE 5173
CMD ["yarn", "dev"]