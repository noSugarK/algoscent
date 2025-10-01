<!-- src/views/account/ResetPassword.vue -->
<template>
  <div class="login-container">
    <div class="login-card card shadow-lg border-0">
      <!-- Logo 区域 -->
      <LogoHeader />

      <h2 class="mt-3 fw-bold text-primary">设置新密码</h2>

      <!-- 验证中状态 -->
      <div v-if="loading" class="text-center py-4">
        <div class="spinner-border text-primary" role="status">
          <span class="visually-hidden">验证中...</span>
        </div>
        <p class="mt-2 text-muted">正在验证链接...</p>
      </div>

      <!-- 链接无效 -->
      <div v-else-if="!validLink" class="text-center">
        <i class="bi bi-x-circle-fill text-danger" style="font-size: 3rem;"></i>
        <p class="text-danger fw-bold mb-3 mt-3">链接无效或已过期</p>
        <p class="text-muted mb-4">请重新申请密码重置链接</p>
        <button
            type="button"
            class="btn btn-secondary w-100 mb-3"
            @click="$router.push('/forgot-password')"
        >
          重新申请
        </button>
        <div class="text-center mt-3">
          <a href="#" class="text-decoration-none" @click.prevent="$router.push('/login')">← 返回登录</a>
        </div>
      </div>

      <!-- 重置密码表单 -->
      <div v-else>
        <p class="text-muted mb-4">请输入您的新密码，至少 8 位字符。</p>

        <form @submit.prevent="submitNewPassword" novalidate>
          <!-- 新密码 -->
          <div class="mb-3">
            <label for="password" class="form-label">新密码</label>
            <input
                id="password"
                v-model="password"
                type="password"
                class="form-control border-primary"
                placeholder="至少 8 位"
                minlength="8"
                required
            />
          </div>

          <!-- 确认新密码 -->
          <div class="mb-3">
            <label for="confirmPassword" class="form-label">确认新密码</label>
            <input
                id="confirmPassword"
                v-model="confirmPassword"
                type="password"
                class="form-control border-primary"
                placeholder="请再次输入"
                required
            />
          </div>

          <!-- 错误提示 -->
          <div v-if="error" class="alert alert-danger small p-2 mb-3">
            {{ error }}
          </div>

          <!-- 提交按钮 -->
          <button
              type="submit"
              :disabled="submitting"
              class="btn btn-gradient w-100 mb-3 shadow-sm"
          >
            <span v-if="submitting" class="spinner-border spinner-border-sm me-2"></span>
            {{ submitting ? '保存中...' : '保存新密码' }}
          </button>
        </form>

        <div class="text-center mt-3">
          <a href="#" class="text-decoration-none" @click.prevent="$router.push('/login')">← 返回登录</a>
        </div>

        <AccountFooter />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import AccountService from '@/api/account.api.js'
import LogoHeader from "@/components/common/LogoHeader.vue"
import AccountFooter from "@/components/layout/AccountFooter.vue"

const route = useRoute()
const router = useRouter()

// URL 参数
const uid = ref(route.params.uid)
const token = ref(route.params.token)

// 页面状态
const loading = ref(true)
const validLink = ref(false)
const submitting = ref(false)
const error = ref('')

// 表单数据
const password = ref('')
const confirmPassword = ref('')

// 检查链接有效性
onMounted(async () => {
  if (!uid.value || !token.value) {
    loading.value = false
    return
  }

  try {
    const res = await AccountService.validatePasswordResetToken(uid.value, token.value)
    validLink.value = res.valid
  } catch (err) {
    console.error('验证失败:', err)
    validLink.value = false
  } finally {
    loading.value = false
  }
})

// 提交新密码（集中验证）
const submitNewPassword = () => {
  error.value = ''

  if (password.value.length < 8) {
    error.value = '密码至少 8 位'
    return
  }
  if (password.value !== confirmPassword.value) {
    error.value = '两次输入的密码不一致'
    return
  }

  submitting.value = true

  AccountService.resetPassword(uid.value, token.value, password.value)
      .then(() => {
        alert('密码已重置，请使用新密码登录')
        router.push('/login')
      })
      .catch((err) => {
        error.value = err.response?.data?.message || '重置失败，请重新申请'
      })
      .finally(() => {
        submitting.value = false
      })
}
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  padding: 20px;
}

.login-card {
  width: 100%;
  max-width: 450px;
  padding: 2.5rem;
  border-radius: 15px;
  background-color: rgb(244, 248, 240);
  backdrop-filter: blur(10px);
  box-shadow: 0 15px 35px rgba(0, 0, 0, 0.2);
  animation: float 3s ease-in-out infinite;
}

@keyframes float {
  0% { transform: translateY(0px); }
  50% { transform: translateY(-10px); }
  100% { transform: translateY(0px); }
}

/* 渐变按钮（仅保留核心样式） */
.btn-gradient {
  background: linear-gradient(135deg, #667eea, #764ba2);
  border: none;
  color: white;
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  font-weight: 500;
  letter-spacing: 1px;
  transition: all 0.3s ease;
}

.btn-gradient:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

.btn-gradient:active:not(:disabled) {
  transform: translateY(0);
}

.btn-gradient:disabled {
  opacity: 0.7;
  cursor: not-allowed;
  transform: none;
}

/* 表单输入框增强 */
.form-control.border-primary {
  border-width: 2px !important;
}
</style>