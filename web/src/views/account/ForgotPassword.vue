<template>
  <div class="login-container">
    <div class="login-card card shadow-lg border-0">
      <!-- Logo 区域 -->
      <LogoHeader />
      
      <h2 class="mt-3 fw-bold text-center text-primary animate__animated animate__fadeInUp">忘记密码</h2>
      
      <!-- 步骤 1：输入用户名 -->
      <div v-if="step === 1" class="animate__animated animate__fadeIn">
        <p class="text-muted mb-4 animate__animated animate__fadeInUp">
          请输入您的用户名进行验证
        </p>
        <form @submit.prevent="checkUsername">
          <div class="mb-3 animate__animated animate__fadeInLeft">
            <label for="username" class="form-label">用户名</label>
            <input
                id="username"
                v-model="username"
                type="text"
                class="form-control custom-input"
                placeholder="请输入用户名"
                required
            />
          </div>
          <button
              type="submit"
              :disabled="loading"
              class="btn custom-btn w-100 mb-3 animate__animated animate__pulse animate__delay-1s"
          >
            <span v-if="loading" class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
            {{ loading ? '验证中...' : '验证用户名' }}
          </button>
        </form>
        <div class="text-center mt-3 animate__animated animate__fadeInUp animate__delay-2s">
          <a href="#" class="text-decoration-none" @click.prevent="$router.push('/login')">← 返回登录</a>
        </div>
      </div>

      <!-- 步骤 2：输入邮箱 -->
      <div v-if="step === 2" class="animate__animated animate__fadeIn">
        <p class="text-muted mb-4 animate__animated animate__fadeInUp">
          请输入您注册时使用的邮箱进行验证
        </p>
        <form @submit.prevent="checkEmail">
          <div class="mb-3 animate__animated animate__fadeInLeft">
            <label for="resetEmail" class="form-label">邮箱地址</label>
            <input
                id="resetEmail"
                v-model="email"
                type="email"
                class="form-control custom-input"
                placeholder="example@company.com"
                required
            />
          </div>
          <button
              type="submit"
              :disabled="loading"
              class="btn custom-btn w-100 mb-3 animate__animated animate__pulse animate__delay-1s"
          >
            <span v-if="loading" class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
            {{ loading ? '验证中...' : '验证邮箱并发送重置链接' }}
          </button>
        </form>
        <div class="text-center mt-3 animate__animated animate__fadeInUp animate__delay-2s">
          <a href="#" class="text-decoration-none" @click="step = 1">← 返回上一步</a> |
          <a href="#" class="text-decoration-none" @click.prevent="$router.push('/login')"> 返回登录</a>
        </div>
      </div>

      <!-- 步骤 3：发送成功 -->
      <div v-if="step === 3" class="animate__animated animate__fadeIn">
        <div class="text-center mb-4">
          <i class="bi bi-check-circle-fill text-success" style="font-size: 3rem;"></i>
        </div>
        <p class="text-success text-center fw-bold mb-3 animate__animated animate__fadeInUp">
          邮件已发送！
        </p>
        <p class="text-muted text-center mb-4 animate__animated animate__fadeInUp animate__delay-1s">
          我们已向 <strong>{{ email }}</strong> 发送了密码重置链接，请查收邮箱（包括垃圾邮件箱）。
        </p>
        <button @click="resendEmail" :disabled="loading" class="btn custom-success-btn w-100 mb-3 animate__animated animate__fadeInUp animate__delay-2s">
          <span v-if="loading" class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
          {{ loading ? '重新发送中...' : '重新发送' }}
        </button>
        <div class="text-center mt-3 animate__animated animate__fadeInUp animate__delay-3s">
          <a href="#" class="text-decoration-none" @click.prevent="$router.push('/login')">← 返回登录</a>
        </div>
      </div>
      <AccountFooter />
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import AccountService from '@/api/account.api.js'
import LogoHeader from "@/components/common/LogoHeader.vue";
import AccountFooter from "@/components/layout/AccountFooter.vue";

const router = useRouter()
const step = ref(1) // 1: 输入用户名, 2: 输入邮箱, 3: 成功提示
const username = ref('')
const email = ref('')
const loading = ref(false)

const checkUsername = async () => {
  if (!username.value) {
    alert('请输入用户名')
    return
  }

  loading.value = true
  try {
    const response = await AccountService.checkUsername(username.value)
    if (response.valid) {
      step.value = 2
      // 不再自动填充邮箱，让用户手动输入
    } else {
      alert('用户名不存在')
    }
  } catch (err) {
    const msg = err.response?.data?.username || '验证失败，请稍后重试'
    alert(msg)
  } finally {
    loading.value = false
  }
}

const checkEmail = async () => {
  if (!email.value) {
    alert('请输入邮箱')
    return
  }

  loading.value = true
  try {
    // 验证邮箱是否与用户名匹配
    const response = await AccountService.checkEmail(username.value, email.value)
    if (response.valid) {
      // 用户名和邮箱都验证通过，发送重置链接
      await AccountService.forgotPassword(email.value)
      step.value = 3
    } else {
      alert('邮箱与用户名不匹配')
    }
  } catch (err) {
    const msg = err.response?.data?.detail || '验证失败，请稍后重试'
    alert(msg)
  } finally {
    loading.value = false
  }
}

const sendResetLink = async () => {
  if (!email.value) {
    alert('请输入邮箱')
    return
  }

  loading.value = true
  try {
    await AccountService.forgotPassword(email.value)
    step.value = 3
  } catch (err) {
    const msg = err.response?.data?.email || '发送失败，请稍后重试'
    alert(msg)
  } finally {
    loading.value = false
  }
}

const resendEmail = () => {
  sendResetLink()
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

/* 自定义输入框样式 (继承自登录页) */
.custom-input {
  transition: all 0.3s ease;
  border: 2px solid #ced4da;
  padding: 0.5rem 0.75rem;
  border-radius: 8px;
}
.custom-input:focus {
  border-color: #0d6efd;
  box-shadow: 0 0 0 0.25rem rgba(13, 110, 253, 0.25);
  outline: 0;
}
.custom-input:hover:not(:focus) {
  border-color: #86b7fe;
}

/* 自定义主按钮样式 (继承自登录页) */
.custom-btn {
  background-color: #0d6efd;
  border-color: #0d6efd;
  color: white;
  padding: 0.75rem 1.5rem;
  font-size: 1rem;
  border-radius: 8px;
  transition: all 0.3s ease;
  font-weight: 500;
  letter-spacing: 1px;
}
.custom-btn:hover:not(:disabled) {
  background-color: #0b5ed7;
  border-color: #0a58ca;
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}
.custom-btn:active:not(:disabled) {
  background-color: #0a58ca;
  border-color: #0a53be;
  transform: translateY(0);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}
.custom-btn:disabled {
  background-color: #6c757d;
  border-color: #6c757d;
  opacity: 0.65;
  cursor: not-allowed;
}

/* --- 新增：自定义成功按钮样式 --- */
.custom-success-btn {
  background-color: #198754; /* Bootstrap success green */
  border-color: #198754;
  color: white;
  padding: 0.75rem 1.5rem;
  font-size: 1rem;
  border-radius: 8px;
  transition: all 0.3s ease;
  font-weight: 500;
  letter-spacing: 1px;
}
.custom-success-btn:hover:not(:disabled) {
  background-color: #157347; /* 深一点的绿色 */
  border-color: #146c43;
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}
.custom-success-btn:active:not(:disabled) {
  background-color: #146c43;
  border-color: #13653f;
  transform: translateY(0);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}
.custom-success-btn:disabled {
  background-color: #6c757d;
  border-color: #6c757d;
  opacity: 0.65;
  cursor: not-allowed;
}

</style>