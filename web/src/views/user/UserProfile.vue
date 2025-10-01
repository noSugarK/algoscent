<template>
  <AppHeader />
  <div class="user-profile-container">
    <el-card class="profile-card">
      <template #header>
        <div class="card-header">
          <span>个人信息</span>
          <el-button
              type="primary"
              @click="handleEditProfile"
          >
            编辑信息
          </el-button>
        </div>
      </template>

      <el-descriptions :column="1" border>
        <el-descriptions-item label="用户名">
          {{ user.username }}
        </el-descriptions-item>
        <el-descriptions-item label="姓名">
          {{ user.full_name || '未设置' }}
        </el-descriptions-item>
        <el-descriptions-item label="邮箱">
          {{ user.email || '未设置' }}
        </el-descriptions-item>
        <el-descriptions-item label="手机号">
          {{ user.phone || '未设置' }}
        </el-descriptions-item>
        <el-descriptions-item label="用户类型">
          <el-tag :type="getUserTypeTagType()">
            {{ getUserTypeText() }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="账户状态">
          <el-tag :type="user.is_active ? 'success' : 'danger'">
            {{ user.is_active ? '激活' : '未激活' }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="创建时间">
          {{ formatDate(user.date_joined) }}
        </el-descriptions-item>
        <el-descriptions-item label="最后登录">
          {{ user.last_login ? formatDate(user.last_login) : '从未登录' }}
        </el-descriptions-item>
      </el-descriptions>
    </el-card>
  </div>
  <AppFooter />
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAccountStore } from '@/stores/account.js'
import UserService from '@/api/user.api.js'
import { ElMessage } from 'element-plus'
import AppHeader from "@/components/layout/AppHeader.vue";

const router = useRouter()
const authStore = useAccountStore()

const user = ref({})

// 获取当前用户信息
const loadUserProfile = async () => {
  try {
    const data = await UserService.getProfile()
    user.value = data
  } catch (error) {
    ElMessage.error('获取用户信息失败')
  }
}

// 格式化日期
const formatDate = (dateString) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  return date.toLocaleString('zh-CN')
}

// 获取用户类型文本
const getUserTypeText = () => {
  if (user.value?.is_superuser) return '超级管理员'
  if (user.value?.is_staff) return '管理员'
  return '普通用户'
}

// 获取用户类型标签类型
const getUserTypeTagType = () => {
  if (user.value?.is_superuser) return 'danger'
  if (user.value?.is_staff) return 'warning'
  return 'info'
}

// 处理编辑信息 - 跳转到编辑页面
const handleEditProfile = () => {
  router.push('/profile/edit')
}

onMounted(() => {
  loadUserProfile()
})
</script>

<style scoped>
.user-profile-container {
  padding: 20px;
  max-width: 800px;
  margin: 0 auto;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.profile-card {
  margin-bottom: 20px;
}
</style>
