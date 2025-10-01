<template>
  <AppHeader />
  <div class="container py-4">
    <div class="row justify-content-center">
      <div class="col-md-8">
        <div class="card">
          <div class="card-header">
            <h5 class="mb-0">修改个人信息</h5>
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
                        disabled
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

                <!-- 当前密码 -->
                <div class="col-12">
                  <label for="currentPassword" class="form-label">当前密码 <span class="text-muted">(修改信息需要验证当前密码)</span></label>
                  <input
                      type="password"
                      class="form-control"
                      id="currentPassword"
                      placeholder=""
                      v-model="form.current_password"
                      required
                  >
                  <div class="invalid-feedback">
                    请输入当前密码以验证身份。
                  </div>
                </div>

                <!-- 新密码 -->
                <div class="col-12">
                  <label for="newPassword" class="form-label">新密码 <span class="text-muted">(不修改请留空)</span></label>
                  <input
                      type="password"
                      class="form-control"
                      id="newPassword"
                      placeholder=""
                      v-model="form.new_password"
                  >
                </div>

                <!-- 确认新密码 -->
                <div class="col-12">
                  <label for="confirmPassword" class="form-label">确认新密码</label>
                  <input
                      type="password"
                      class="form-control"
                      id="confirmPassword"
                      placeholder=""
                      v-model="form.confirm_password"
                      :required="!!form.new_password"
                  >
                  <div class="invalid-feedback">
                    两次输入的密码必须一致。
                  </div>
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
import { ref, reactive, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import UserService from '@/api/user.api.js'
import AppHeader from '@/components/layout/AppHeader.vue'
import AppFooter from '@/components/layout/AppFooter.vue'
import { useRouter } from 'vue-router'

const router = useRouter()

// 定义响应式数据
const form = reactive({
  username: '',
  full_name: '',
  email: '',
  phone: '',
  current_password: '',
  new_password: '',
  confirm_password: ''
})

const user = ref(null)
// 加载状态
const loading = ref(false)

// 获取当前用户信息
const loadUserProfile = async () => {
  try {
    const data = await UserService.getProfile()
    user.value = data
    form.username = data.username || ''
    form.full_name = data.full_name || ''
    form.email = data.email || ''
    form.phone = data.phone || ''
  } catch (error) {
    ElMessage.error('获取用户信息失败')
  }
}

// 处理表单提交
const handleSubmit = async () => {
  // 验证密码确认
  if (form.new_password && form.new_password !== form.confirm_password) {
    ElMessage.error('两次输入的密码不一致')
    return
  }

  // 验证当前密码
  if (!form.current_password) {
    ElMessage.error('修改信息需要验证当前密码')
    return
  }

  loading.value = true

  try {
    // 构造要提交的数据
    const userData = {
      full_name: form.full_name,
      email: form.email,
      phone: form.phone,
      current_password: form.current_password
    }

    // 如果有新密码，添加到数据中
    if (form.new_password) {
      userData.password = form.new_password
    }

    const result = await UserService.updateProfile(userData)
    ElMessage.success('信息更新成功')
    // 更新auth store中的用户信息
    // 这里可以调用accountStore.setUser(result)来更新用户信息
    router.push('/profile')
  } catch (error) {
    console.error('更新失败:', error)
    ElMessage.error(error.response?.data?.detail || error.message || '更新失败')
  } finally {
    loading.value = false
  }
}

// 取消编辑
const cancelEdit = () => {
  router.push('/profile')
}

onMounted(() => {
  loadUserProfile()
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
