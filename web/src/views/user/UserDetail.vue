<template>
  <AppHeader />
  <div class="user-detail-container">
    <el-card class="detail-card">
      <template #header>
        <div class="card-header">
          <span>用户详情</span>
          <div>
            <el-button class="me-2" @click="editUser">
              编辑
            </el-button>
            <el-button type="danger" @click="deleteUser" :disabled="user && user.id === currentUser.id">
              删除
            </el-button>
            <el-button @click="goBack">返回</el-button>
          </div>
        </div>
      </template>

      <el-skeleton :loading="loading" animated>
        <template #template>
          <el-descriptions :column="1" border>
            <el-descriptions-item label="用户名">
              <el-skeleton-item variant="text" style="width: 30%" />
            </el-descriptions-item>
            <el-descriptions-item label="姓名">
              <el-skeleton-item variant="text" style="width: 30%" />
            </el-descriptions-item>
            <el-descriptions-item label="邮箱">
              <el-skeleton-item variant="text" style="width: 50%" />
            </el-descriptions-item>
            <el-descriptions-item label="手机号">
              <el-skeleton-item variant="text" style="width: 30%" />
            </el-descriptions-item>
            <el-descriptions-item label="用户类型">
              <el-skeleton-item variant="text" style="width: 20%" />
            </el-descriptions-item>
            <el-descriptions-item label="账户状态">
              <el-skeleton-item variant="text" style="width: 20%" />
            </el-descriptions-item>
            <el-descriptions-item label="创建时间">
              <el-skeleton-item variant="text" style="width: 40%" />
            </el-descriptions-item>
            <el-descriptions-item label="最后登录">
              <el-skeleton-item variant="text" style="width: 40%" />
            </el-descriptions-item>
            <el-descriptions-item label="创建者">
              <el-skeleton-item variant="text" style="width: 30%" />
            </el-descriptions-item>
          </el-descriptions>
        </template>

        <template #default>
          <div v-if="user">
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
                <el-tag :type="getUserTypeTagType(user)">
                  {{ getUserTypeText(user) }}
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
              <el-descriptions-item label="创建者" v-if="user.creator">
                {{ user.creator.username }}
              </el-descriptions-item>
            </el-descriptions>
          </div>
        </template>
      </el-skeleton>
    </el-card>
  </div>
  <AppFooter />
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import UserService from '@/api/user.api.js'
import { ElMessage, ElMessageBox } from 'element-plus'
import { useAccountStore } from '@/stores/account.js'
import AppHeader from '@/components/layout/AppHeader.vue'
import AppFooter from '@/components/layout/AppFooter.vue'

const route = useRoute()
const router = useRouter()
const accountStore = useAccountStore()
const currentUser = computed(() => accountStore.user)

const loading = ref(false)
const user = ref(null)

const userId = route.params.id

// 获取用户详情
const loadUserDetail = async () => {
  if (!userId) {
    ElMessage.error('用户ID无效')
    router.push('/users')
    return
  }

  loading.value = true
  try {
    const data = await UserService.getUserDetail(userId)
    user.value = data
  } catch (error) {
    ElMessage.error(error.message || '获取用户详情失败')
    router.push('/users')
  } finally {
    loading.value = false
  }
}

// 编辑用户
const editUser = () => {
  if (!user.value) return
  router.push(`/users/${user.value.id}/edit`)
}

// 删除用户
const deleteUser = () => {
  if (!user.value) return

  ElMessageBox.confirm(
      `确定要删除用户 "${user.value.username}" 吗？此操作不可恢复！`,
      '确认删除',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
      }
  ).then(async () => {
    try {
      await UserService.deleteUser(user.value.id)
      ElMessage.success('用户删除成功')
      router.push('/users')
    } catch (error) {
      ElMessage.error(error.message || '删除用户失败')
    }
  }).catch(() => {
    // 用户取消删除
  })
}

// 获取用户类型文本
const getUserTypeText = (user) => {
  if (user.is_superuser) return '超级管理员'
  if (user.is_staff) return '管理员'
  return '普通用户'
}

// 获取用户类型标签类型
const getUserTypeTagType = (user) => {
  if (user.is_superuser) return 'danger'
  if (user.is_staff) return 'warning'
  return 'info'
}

// 格式化日期
const formatDate = (dateString) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  return date.toLocaleString('zh-CN')
}

// 返回上一页
const goBack = () => {
  router.go(-1)
}

onMounted(() => {
  loadUserDetail()
})
</script>

<style scoped>
.user-detail-container {
  padding: 20px;
  max-width: 800px;
  margin: 0 auto;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.detail-card {
  margin-bottom: 20px;
}
</style>
