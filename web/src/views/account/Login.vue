<!-- src/views/account/Login.vue -->
<template>
  <div class="login-container d-flex">
    <!-- 左侧登录表单 -->
    <div class="login-form-wrapper d-flex align-items-center justify-content-center flex-grow-1">
      <div class="login-card card shadow-lg border-0 p-4">
        <a href="/" class="d-flex justify-content-center mb-3">
          <LogoHeader />
        </a>
        <h2 class="fw-bold text-primary text-center mb-4">欢迎登录</h2>

        <form @submit.prevent="handleLogin" novalidate>
          <!-- 用户名 -->
          <div class="mb-3">
            <label for="username" class="form-label">用户名</label>
            <input
                id="username"
                v-model="form.username"
                type="text"
                class="form-control border-primary"
                placeholder="请输入用户名"
                required
            />
            <div class="invalid-feedback">请输入用户名</div>
          </div>

          <!-- 密码 -->
          <div class="mb-3">
            <label for="password" class="form-label">密码</label>
            <input
                id="password"
                v-model="form.password"
                type="password"
                class="form-control border-primary"
                placeholder="请输入密码"
                required
            />
            <div class="invalid-feedback">请输入密码</div>
          </div>

          <!-- 记住我 + 忘记密码 -->
          <div class="d-flex justify-content-between align-items-center mb-3">
            <div class="form-check">
              <input
                  id="remember_me"
                  v-model="form.remember_me"
                  class="form-check-input"
                  type="checkbox"
                  style="accent-color: #0d6efd"
              />
              <label class="form-check-label" for="remember_me">记住我</label>
            </div>
            <a href="#" class="text-decoration-none text-primary" @click.prevent="gotoForgotPassword">
              忘记密码？
            </a>
          </div>

          <!-- 登录按钮 -->
          <button
              type="submit"
              :disabled="loading"
              class="btn btn-primary w-100 mb-3 shadow-sm btn-login"
          >
            <span v-if="loading" class="spinner-border spinner-border-sm me-2"></span>
            {{ loading ? '登录中...' : '登 录' }}
          </button>

          <!-- 第三方登录 -->
          <div class="text-center mt-4">
            <p class="text-muted">或使用以下方式登录</p>
            <div class="d-flex justify-content-center gap-3">
              <button class="btn btn-outline-secondary btn-sm rounded-circle social-btn">
                <i class="fa-brands fa-weixin"></i>
              </button>
              <button class="btn btn-outline-secondary btn-sm rounded-circle social-btn">
                <i class="fa-brands fa-weibo"></i>
              </button>
              <button class="btn btn-outline-secondary btn-sm rounded-circle social-btn">
                <i class="fa-brands fa-qq"></i>
              </button>
            </div>
          </div>
        </form>

        <AccountFooter />
      </div>
    </div>

    <Qrcode />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAccountStore } from '@/stores/account.js'
import { JSEncrypt } from 'encryptlong'
import AccountService from '@/api/account.api.js'
import LogoHeader from "@/components/common/LogoHeader.vue";
import AccountFooter from "@/components/layout/AccountFooter.vue";
import Qrcode from "@/components/account/Qrcode.vue";

const router = useRouter()
const accountStore = useAccountStore()

const form = ref({
  username: '',
  password: '',
  remember_me: false,
})

const loading = ref(false)
const publicKey = ref('')

onMounted(async () => {
  try {
    const res = await AccountService.getPublicKey()
    publicKey.value = res.public_key
    console.log('✅ 公钥加载成功')
  } catch (err) {
    console.error('❌ 获取公钥失败:', err)
    alert('系统初始化失败，请刷新重试！')
  }
})

const gotoForgotPassword = () => {
  router.push('/forgot-password')
}

const handleLogin = async () => {
  const usernameEl = document.getElementById('username')
  const passwordEl = document.getElementById('password')

  usernameEl.classList.remove('is-invalid')
  passwordEl.classList.remove('is-invalid')

  if (!form.value.username) {
    usernameEl.classList.add('is-invalid')
    return
  }
  if (!form.value.password) {
    passwordEl.classList.add('is-invalid')
    return
  }

  if (!publicKey.value) {
    alert('公钥未加载，请稍后重试')
    return
  }

  if (!form.value.username || !form.value.password) {
    alert('请填写用户名和密码')
    return
  }

  loading.value = true

  try {
    // 🔐 创建加密器
    const encryptor = new JSEncrypt()
    encryptor.setPublicKey(publicKey.value)

  const encryptedUsername = encryptor.encrypt(form.value.username)
  const encryptedPassword = encryptor.encrypt(form.value.password)

  if (!encryptedUsername || !encryptedPassword) {
    alert('加密失败，请检查输入')
    loading.value = false
    return
  }

    // 🔁 发送加密后的请求
    const res = await AccountService.login(encryptedUsername, encryptedPassword, form.value.remember_me)

    // ✅ 登录成功
    const { access, refresh, user } = res
    accountStore.setTokens(access, refresh)
    accountStore.setUser(user)

    // 跳转首页
    router.push('/')
  } catch (err) {
    const errorMsg =
        err.response?.data?.detail || '登录失败，请检查用户名或密码'
    alert(errorMsg)
    console.error('登录错误:', err)
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
}

/* 左侧登录表单区域 */
.login-form-wrapper {
  max-width: 500px;
}

.login-card {
  width: 100%;
  max-width: 450px;
  padding: 2.5rem;
  border-radius: 15px;
  backdrop-filter: blur(10px);
  box-shadow: 0 15px 35px rgba(0, 0, 0, 0.2);
  animation: float 3s ease-in-out infinite;
}

@keyframes float {
  0% { transform: translateY(0px); }
  50% { transform: translateY(-10px); }
  100% { transform: translateY(0px); }
}

/* 按钮增强 */
.btn-login {
  padding: 0.75rem 1.5rem;
  font-size: 1rem;
  border-radius: 8px;
  font-weight: 500;
  transition: all 0.3s ease;
}

.btn-login:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.btn-login:active:not(:disabled) {
  transform: translateY(0);
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
}

/* 社交按钮 */
.social-btn {
  width: 45px;
  height: 45px;
  border-width: 2px;
  transition: all 0.2s ease;
}

.social-btn:hover {
  transform: scale(1.1);
  border-color: #0d6efd;
  background-color: #e7f1ff;
}

/* 响应式：小屏幕下隐藏右侧卡片 */
@media (max-width: 992px) {
  .login-container {
    flex-direction: column;
    padding: 20px 0;
  }

  .introduction-card {
    display: none !important;
  }

  .login-form-wrapper {
    width: 100%;
  }
}
</style>