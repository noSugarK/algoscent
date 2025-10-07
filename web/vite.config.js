// vite.config.js
import { fileURLToPath, URL } from 'node:url'
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueDevTools from 'vite-plugin-vue-devtools'
import AutoImport from 'unplugin-auto-import/vite'
import Components from 'unplugin-vue-components/vite'
import { ElementPlusResolver } from 'unplugin-vue-components/resolvers'


// https://vite.dev/config/
export default defineConfig({
    plugins: [
        vue(),
        vueDevTools(),
        AutoImport({
            resolvers: [ElementPlusResolver()],
        }),
        Components({
            resolvers: [ElementPlusResolver()],
        }),
    ],
    resolve: {
        alias: {
            '@': fileURLToPath(new URL('./src', import.meta.url))
        },
    },
    // 添加服务器配置和代理
    server: {
        // 开发服务器端口
        port: 5173,
        // 启动时自动打开浏览器
        open: true,
        // 配置代理解决跨域问题
        proxy: {
            // 将 /api 开头的请求代理到后端服务器
            '/api': {
                target: 'http://localhost:8000', // Django后端地址
                changeOrigin: true,
                // 重写路径，去掉 /api 前缀（如果需要的话）
                rewrite: (path) => path.replace(/^\/api/, '')
            }
        }
    }
})
