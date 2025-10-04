<template>
  <header class="app-header text-bg-success">
    <div class="container">
      <div class="d-flex flex-wrap align-items-center justify-content-center justify-content-lg-start py-2 mb-0">
        <!-- Logo -->
        <a class="navbar-brand d-flex align-items-center text-white" href="/">
          <LogoHeader />
        </a>

        <!-- Navigation Links -->
        <ul class="nav col-12 col-lg-auto me-lg-auto mb-2 mb-md-0 justify-content-center">
          <li><a href="#" class="nav-link px-2" :class="{ 'text-secondary': isActive('/') }" @click.prevent="goTo('/')">首页</a></li>
          <li><a href="#" class="nav-link px-2 text-white" :class="{ 'text-secondary': isActive('/quiz') }" @click.prevent="goTo('/quiz')">香氛测试</a></li>
          <li><a href="#" class="nav-link px-2 text-white" :class="{ 'text-secondary': isActive('/products') }" @click.prevent="goTo('/products')">产品系列</a></li>
          <li><a href="#" class="nav-link px-2 text-white" :class="{ 'text-secondary': isActive('/about') }" @click.prevent="goTo('/about')">关于我们</a></li>
        </ul>

        <!-- Search Form -->
        <!-- form class="col-12 col-lg-auto mb-3 mb-lg-0 me-lg-3" role="search">
          <input
              type="search"
              class="form-control form-control-dark text-bg-dark"
              placeholder="Search..."
              aria-label="Search"
              v-model="searchQuery"
              @keyup.enter="handleSearch"
          />
        </form -->

        <!-- Auth Buttons or User Dropdown -->
        <div class="d-flex align-items-center ms-lg-auto" v-if="!accountStore.isAuthenticated">
          <button type="button" class="btn btn-outline-light me-2" @click="$router.push('/login')">登录</button>
          <button type="button" class="btn btn-warning" @click="$router.push('/register')">注册</button>
        </div>

        <div class="d-flex align-items-center ms-lg-auto" v-else>
          <el-dropdown @command="handleUserCommand">
            <span class="el-dropdown-link nav-link px-2 text-white d-flex align-items-center">
              {{ accountStore.user?.username }}
              <el-icon class="el-icon--right"><ArrowDown /></el-icon>
            </span>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item command="profile">个人中心</el-dropdown-item>
                <el-dropdown-item command="profile-edit">修改信息</el-dropdown-item>
                <el-dropdown-item command="user-list" v-if="accountStore.user?.is_staff || accountStore.user?.is_superuser">用户列表</el-dropdown-item>
                <el-dropdown-item divided command="logout">退出登录</el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </div>
    </div>
  </header>
</template>

<script setup>
import { ref } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useAccountStore } from '@/stores/account.js';
import { ArrowDown } from '@element-plus/icons-vue';
import LogoHeader from '../common/LogoHeader.vue';

const route = useRoute();
const router = useRouter();
const accountStore = useAccountStore();
const searchQuery = ref('');

const goTo = (path) => {
  router.push(path);
};

const isActive = (path) => {
  return route.path === path;
};

const handleSearch = () => {
  if (searchQuery.value.trim()) {
    // 示例：跳转到搜索页或触发事件
    router.push({ path: '/search', query: { q: searchQuery.value } });
  }
};

const handleUserCommand = (command) => {
  switch (command) {
    case 'logout':
      accountStore.clear();
      router.push('/login');
      break;
    case 'profile':
      router.push('/profile');
      break;
    case 'profile-edit':
      router.push('/profile/edit');
      break;
    case 'settings':
      router.push('/settings');
      break;
    case 'help':
      console.log('打开帮助文档');
      break;
    case 'user-list':
      router.push('/users');
      break;
    default:
      break;
  }
};
</script>

<style scoped>
.nav-link {
  color: #dee2e6 !important;
  transition: color 0.15s ease-in-out;
}

.nav-link:hover,
.nav-link:focus {
  color: #fff !important;
}

.nav-link.text-secondary {
  color: #619c38 !important; /* Secondary color for active link */
  pointer-events: none;
  cursor: default;
}

/* Ensure dropdown link inherits white color */
.el-dropdown-link.text-white {
  color: #dee2e6 !important;
}

.el-dropdown-link.text-white:hover {
  color: #fff !important;
}
</style>