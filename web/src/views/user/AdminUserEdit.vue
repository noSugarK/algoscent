<template>
  <AppHeader />
  <div class="container py-4">
    <div class="row justify-content-center">
      <div class="col-md-8">
        <div class="card">
          <div class="card-header">
            <h5 class="mb-0">修改用户信息</h5>
          </div>
          <div class="card-body">
            <form class="needs-validation" novalidate @submit.prevent="handleSubmit">
              <div class="row g-3">
                <!-- 用户名 -->
                <div class="col-sm-6">
                  <label for="username" class="form-label">用户名</label>
                  <div class="input-group has-validation">
                    <span class="input-group-text">@</span>
                    <input
                        type="text"
                        class="form-control"
                        id="username"
                        placeholder="Username"
                        v-model="form.username"
                        required
                    >
                    <div class="invalid-feedback">
                      用户名是必需的。
                    </div>
                  </div>
                </div>

                <!-- 姓名 -->
                <div class="col-sm-6">
                  <label for="fullName" class="form-label">姓名</label>
                  <input
                      type="text"
                      class="form-control"
                      id="fullName"
                      placeholder=""
                      v-model="form.full_name"
                      required
                  >
                  <div class="invalid-feedback">
                    请输入有效姓名。
                  </div>
                </div>

                <!-- 邮箱 -->
                <div class="col-12">
                  <label for="email" class="form-label">邮箱</label>
                  <input
                      type="email"
                      class="form-control"
                      id="email"
                      placeholder="you@example.com"
                      v-model="form.email"
                      required
                  >
                  <div class="invalid-feedback">
                    请输入有效的邮箱地址。
                  </div>
                </div>

                <!-- 手机号 -->
                <div class="col-12">
                  <label for="phone" class="form-label">手机号</label>
                  <input
                      type="tel"
                      class="form-control"
                      id="phone"
                      placeholder=""
                      v-model="form.phone"
                  >
                </div>

                <!-- 用户类型 -->
                <div class="col-12">
                  <label for="userType" class="form-label">用户类型</label>
                  <select class="form-select" id="userType" v-model="form.user_type">
                    <option value="user">普通用户</option>
                    <option value="staff" v-if="isSuperuser">管理员</option>
                    <option value="superuser" v-if="isSuperuser">超级管理员</option>
                  </select>
                </div>

                <!-- 重置密码按钮 -->
                <div class="col-12">
                  <button type="button" class="btn btn-warning" @click="resetPassword" :disabled="loading">
                    重置密码为默认密码 (hbsz@123)
                  </button>
                </div>
              </div>

              <hr class="my-4">

              <div class="d-flex justify-content-between">
                <button class="btn btn-secondary" type="button" @click="cancelEdit">
                  取消
                </button>
                <button class="btn btn-primary" type="submit" :disabled="loading">
                  <span v-if="loading" class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
                  保存更改
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
  <AppFooter />
</template>

<script setup>
import { ref, reactive, watch, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import UserService from '@/api/user.api.js'
import { useAccountStore } from '@/stores/account.js'
import AppHeader from '@/components/layout/AppHeader.vue'
import AppFooter from '@/components/layout/AppFooter.vue'
import { useRoute, useRouter } from 'vue-router'

// 获取路由实例
const route = useRoute()
const router = useRouter()

// 获取账户存储
const accountStore = useAccountStore()
const isSuperuser = accountStore.user.is_superuser

// 定义响应式数据
const form = reactive({
  username: '',
  full_name: '',
  email: '',
  phone: '',
  user_type: 'user'
})

const user = ref(null)
// 加载状态
const loading = ref(false)

// 获取用户详情
const loadUserDetail = async () => {
  const userId = route.params.id
  if (!userId) {
    ElMessage.error('用户ID无效')
    return
  }

  try {
    const data = await UserService.getUserDetail(userId)
    user.value = data

    // 填充表单数据
    form.username = data.username || ''
    form.full_name = data.full_name || ''
    form.email = data.email || ''
    form.phone = data.phone || ''

    // 设置用户类型
    if (data.is_superuser) {
      form.user_type = 'superuser'
    } else if (data.is_staff) {
      form.user_type = 'staff'
    } else {
      form.user_type = 'user'
    }
  } catch (error) {
    ElMessage.error(error.message || '获取用户详情失败')
  }
}

// 处理表单提交
const handleSubmit = async () => {
  loading.value = true

  try {
    // 构造要提交的数据
    const userData = {
      username: form.username,
      full_name: form.full_name,
      email: form.email,
      phone: form.phone
    }

    // 更新用户类型（仅超级管理员）
    if (isSuperuser) {
      if (form.user_type === 'superuser') {
        userData.is_superuser = true
        userData.is_staff = true
      } else if (form.user_type === 'staff') {
        userData.is_superuser = false
        userData.is_staff = true
      } else {
        userData.is_superuser = false
        userData.is_staff = false
      }
    }

    const result = await UserService.updateUser(user.value.id, userData)
    ElMessage.success('信息更新成功')
    router.push(`/users/${user.value.id}`)
  } catch (error) {
    console.error('更新失败:', error)
    ElMessage.error(error.response?.data?.detail || error.message || '更新失败')
  } finally {
    loading.value = false
  }
}

// 重置密码
const resetPassword = async () => {
  ElMessageBox.confirm(
      '确定要将该用户的密码重置为默认密码 "hbsz@123" 吗？',
      '确认重置密码',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
      }
  ).then(async () => {
    try {
      loading.value = true
      // 发送完整的用户数据以及新密码
      const userData = {
        username: form.username,
        full_name: form.full_name,
        email: form.email,
        phone: form.phone,
        password: 'hbsz@123'
      }
      
      // 添加用户类型信息
      if (isSuperuser) {
        if (form.user_type === 'superuser') {
          userData.is_superuser = true
          userData.is_staff = true
        } else if (form.user_type === 'staff') {
          userData.is_superuser = false
          userData.is_staff = true
        } else {
          userData.is_superuser = false
          userData.is_staff = false
        }
      }

      const result = await UserService.updateUser(user.value.id, userData)
      ElMessage.success('密码已重置为默认密码')
    } catch (error) {
      ElMessage.error(error.response?.data?.detail || error.message || '重置密码失败')
    } finally {
      loading.value = false
    }
  }).catch(() => {
    // 用户取消操作
  })
}

// 取消编辑
const cancelEdit = () => {
  router.push(`/users/${user.value.id}`)
}

onMounted(() => {
  loadUserDetail()
})
</script>

<style scoped>
.card {
  border: 1px solid #dee2e6;
  border-radius: 0.375rem;
}

.card-header {
  background-color: #f8f9fa;
  border-bottom: 1px solid #dee2e6;
  padding: 1rem 1.25rem;
}

.form-label {
  font-weight: 500;
}

.form-control:focus,
.form-select:focus {
  border-color: #0d6efd;
  box-shadow: 0 0 0 0.25rem rgba(13, 110, 253, 0.25);
}
</style>