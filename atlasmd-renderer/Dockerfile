ARG APP_VERSION

FROM node:lts-alpine

WORKDIR /app
COPY package.json yarn.lock ./

RUN --mount=type=cache,target=/root/.yarn YARN_CACHE_FOLDER=/root/.yarn yarn install

COPY . .

# content/ and public/ are expected to be volume-mounted at runtime
RUN mkdir -p content public

ENV APP_VERSION=${APP_VERSION}
ENV PORT=3003
CMD ["yarn", "run", "dev"]
