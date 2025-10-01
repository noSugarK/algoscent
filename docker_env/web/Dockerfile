FROM node:22-alpine as frontend-builder
WORKDIR /web/
# 先复制package文件以利用缓存
COPY web/package*.json ./
# 直接使用npm安装（不需要安装pnpm）
RUN npm install --frozen-lockfile
# 复制源码
COPY web/. .
# 使用npm运行构建
RUN npm run build

# 构建 Nginx 镜像，将前端项目复制到镜像中
FROM nginx:alpine
COPY ./docker_env/nginx/my.conf /etc/nginx/conf.d/my.conf
COPY --from=frontend-builder /web/dist /usr/share/nginx/html