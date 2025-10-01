<template>
  <AppHeader />
  <div class="container py-4">
    <div class="row justify-content-center">
      <div class="col-md-8">
        <div class="card">
          <div class="card-header">
            <h5 class="mb-0">创建新用户</h5>
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
                      @blur="checkUsername"
                      :class="{
                        'is-invalid': usernameError || (usernameChecked && usernameExists),
                        'is-valid': usernameChecked && !usernameExists && !usernameError
                      }"
                      required
                    >
                    <div class="invalid-feedback" v-if="usernameError">
                      {{ usernameError }}
                    </div>
                    <div class="invalid-feedback" v-else-if="usernameChecked && usernameExists">
                      用户名已存在，请选择其他用户名
                    </div>
                    <div class="valid-feedback" v-else-if="usernameChecked && !usernameExists">
                      用户名可用
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
                    @blur="checkEmail"
                    :class="{
                      'is-invalid': emailError || (emailChecked && emailExists),
                      'is-valid': emailChecked && !emailExists && !emailError
                    }"
                    required
                  >
                  <div class="invalid-feedback" v-if="emailError">
                    {{ emailError }}
                  </div>
                  <div class="invalid-feedback" v-else-if="emailChecked && emailExists">
                    邮箱已被使用，请选择其他邮箱
                  </div>
                  <div class="valid-feedback" v-else-if="emailChecked && !emailExists">
                    邮箱可用
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
                <div class="col-12" v-if="isSuperuser">
                  <label for="userType" class="form-label">用户类型</label>
                  <select class="form-select" id="userType" v-model="form.user_type">
                    <option value="user">普通用户</option>
                    <option value="staff">管理员</option>
                    <!-- <option value="superuser">超级管理员</option> -->
                  </select>
                </div>

                <!-- 密码 -->
                <div class="col-12">
                  <label for="password" class="form-label">密码</label>
                  <div class="input-group">
                    <input 
                      :type="showPassword ? 'text' : 'password'" 
                      class="form-control" 
                      id="password" 
                      placeholder=""
                      v-model="form.password"
                      @blur="validatePassword"
                      :class="{
                        'is-invalid': passwordError,
                        'is-valid': form.password && !passwordError
                      }"
                      required
                    >
                    <div class="invalid-feedback" v-if="passwordError">
                      {{ passwordError }}
                    </div>
                  </div>
                  <div class="form-text">密码长度至少8位，至少包含数字、大小写字母、特殊字符中的任意两种</div>
                </div>

                <!-- 确认密码 -->
                <div class="col-12">
                  <label for="confirmPassword" class="form-label">确认密码</label>
                  <div class="input-group">
                    <input 
                      :type="showConfirmPassword ? 'text' : 'password'" 
                      class="form-control" 
                      id="confirmPassword" 
                      placeholder=""
                      v-model="form.confirm_password"
                      @blur="validateConfirmPassword"
                      :class="{
                        'is-invalid': confirmPasswordError,
                        'is-valid': form.confirm_password && !confirmPasswordError
                      }"
                      required
                    >
                    <div class="invalid-feedback" v-if="confirmPasswordError">
                      {{ confirmPasswordError }}
                    </div>
                  </div>
                </div>
              </div>

              <hr class="my-4">

              <div class="d-flex justify-content-between">
                <button class="btn btn-secondary" type="button" @click="goBack">
                  返回
                </button>
                <button 
                  class="btn btn-primary" 
                  type="submit" 
                  :disabled="loading || !!usernameError || !!emailError || !!passwordError || !!confirmPasswordError || usernameExists || emailExists || !usernameChecked || !emailChecked">
                  <span v-if="loading" class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
                  创建用户
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
import { ref, reactive, watch } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import UserService from '@/api/user.api.js'
import { useAccountStore } from '@/stores/account.js'
import AppHeader from '@/components/layout/AppHeader.vue'
import AppFooter from '@/components/layout/AppFooter.vue'

// 获取路由实例
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
  user_type: 'user',
  password: '',
  confirm_password: ''
})

// 验证状态
const usernameError = ref('')
const emailError = ref('')
const passwordError = ref('')
const confirmPasswordError = ref('')
const usernameExists = ref(false)
const emailExists = ref(false)
const usernameChecked = ref(false)
const emailChecked = ref(false)
const loading = ref(false)

// 验证密码强度
const validatePassword = () => {
  if (!form.password) {
    passwordError.value = '请输入密码'
    return false
  }
  
  // 检查密码长度
  if (form.password.length < 8) {
    passwordError.value = '密码长度至少8位'
    return false
  }
  
  // 检查密码复杂度（至少包含数字、大小写字母、特殊字符中的任意两种）
  const hasLower = /[a-z]/.test(form.password)
  const hasUpper = /[A-Z]/.test(form.password)
  const hasDigit = /\d/.test(form.password)
  const hasSpecial = /[!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]/.test(form.password)
  
  const conditions = [hasLower, hasUpper, hasDigit, hasSpecial].filter(Boolean).length
  
  if (conditions < 2) {
    passwordError.value = '密码至少包含数字、大小写字母、特殊字符中的任意两种'
    return false
  }
  
  passwordError.value = ''
  return true
}

// 验证确认密码
const validateConfirmPassword = () => {
  if (!form.confirm_password) {
    confirmPasswordError.value = '请确认密码'
    return false
  }
  
  if (form.password !== form.confirm_password) {
    confirmPasswordError.value = '两次输入的密码不一致'
    return false
  }
  
  confirmPasswordError.value = ''
  return true
}

// 检查用户名唯一性
const checkUsername = async () => {
  if (!form.username) {
    usernameError.value = '请输入用户名'
    usernameChecked.value = false
    return
  }
  
  // 重置错误信息
  usernameError.value = ''
  
  try {
    const response = await UserService.checkUsernameExists(form.username)
    usernameExists.value = response.exists
    usernameChecked.value = true
  } catch (error) {
    usernameError.value = error.message || '用户名检查失败'
    usernameChecked.value = false
  }
}

// 检查邮箱唯一性
const checkEmail = async () => {
  if (!form.email) {
    emailError.value = '请输入邮箱'
    emailChecked.value = false
    return
  }
  
  // 简单的邮箱格式验证
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  if (!emailRegex.test(form.email)) {
    emailError.value = '请输入有效的邮箱地址'
    emailChecked.value = false
    return
  }
  
  // 重置错误信息
  emailError.value = ''
  
  try {
    const response = await UserService.checkEmailExists(form.email)
    emailExists.value = response.exists
    emailChecked.value = true
  } catch (error) {
    emailError.value = error.message || '邮箱检查失败'
    emailChecked.value = false
  }
}

// 监听密码确认字段
watch(() => form.confirm_password, () => {
  validateConfirmPassword()
})

// 监听密码字段
watch(() => form.password, () => {
  validatePassword()
  // 如果密码改变了，也需要重新验证确认密码
  if (form.confirm_password) {
    validateConfirmPassword()
  }
})

// 处理表单提交
const handleSubmit = async () => {
  // 验证所有字段
  const isPasswordValid = validatePassword()
  const isConfirmPasswordValid = validateConfirmPassword()
  
  if (!isPasswordValid || !isConfirmPasswordValid) {
    ElMessage.error('请检查表单中的错误')
    return
  }

  // 检查必填字段
  if (!form.username || !form.full_name || !form.email) {
    ElMessage.error('请填写所有必填字段')
    return
  }

  // 检查用户名和邮箱是否已存在
  if (usernameExists.value || emailExists.value) {
    ElMessage.error('用户名或邮箱已存在，请修改后重试')
    return
  }

  loading.value = true
  
  try {
    // 构造要提交的数据
    const userData = {
      username: form.username,
      full_name: form.full_name,
      email: form.email,
      phone: form.phone,
      password: form.password
    }
    
    // 添加用户类型（仅超级管理员）
    if (isSuperuser) {
      /*if (form.user_type === 'superuser') {
        userData.is_superuser = true
        userData.is_staff = true
      } else*/ if (form.user_type === 'staff') {
        userData.is_superuser = false
        userData.is_staff = true
      }
    }
    
    const result = await UserService.createUser(userData)
    ElMessage.success('用户创建成功')
    router.push(`/users/${result.id}`)
  } catch (error) {
    console.error('创建失败:', error)
    ElMessage.error(error.message || '创建失败')
  } finally {
    loading.value = false
  }
}

// 返回上一页
const goBack = () => {
  router.go(-1)
}
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

.form-text {
  font-size: 0.875em;
  color: #6c757d;
}
</style>