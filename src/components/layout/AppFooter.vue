<template>
  <footer class="bg-dark text-white py-12">
    <div class="container mx-auto px-4">
      <div class="grid grid-cols-1 md:grid-cols-4 gap-8">
        <div>
          <h3 class="text-xl font-bold mb-4">疗愈香氛</h3>
          <p class="text-gray-400">用自然香气治愈心灵，找回内心平静。</p>
        </div>
        
        <div>
          <h4 class="font-semibold mb-4">快速链接</h4>
          <ul class="space-y-2 text-gray-400">
            <li><router-link to="/" class="hover:text-white">首页</router-link></li>
            <li><router-link to="/quiz" class="hover:text-white">香氛测试</router-link></li>
            <li><a href="#" class="hover:text-white">产品系列</a></li>
          </ul>
        </div>
        
        <div>
          <h4 class="font-semibold mb-4">关于我们</h4>
          <ul class="space-y-2 text-gray-400">
            <li><a href="#" class="hover:text-white">品牌故事</a></li>
            <li><a href="#" class="hover:text-white">联系我们</a></li>
          </ul>
        </div>
        
        <div>
          <h4 class="font-semibold mb-4">关注我们</h4>
          <div class="flex space-x-4">
            <a href="#" class="text-gray-500 hover:text-green-600 transition">
              <i class="fa-brands fa-weixin text-xl"></i>
            </a>
            <a href="#" class="text-gray-500 hover:text-orange-500 transition">
              <i class="fa-brands fa-weibo text-xl"></i>
            </a>
            <a href="#" class="text-gray-500 hover:text-pink-600 transition">
              <i class="fa-brands fa-instagram text-xl"></i>
            </a>
          </div>
        </div>
      </div>
      
      <div class="border-t border-gray-800 mt-8 pt-8 text-center text-gray-500">
        <p>© 2025 疗愈香氛. 保留所有权利.</p>
      </div>
    </div>
  </footer>
</template>

<script setup>
// 页脚组件
</script>

<style scoped>
.bg-dark {
  background-color: #2c2c2c;
}
</style>
    