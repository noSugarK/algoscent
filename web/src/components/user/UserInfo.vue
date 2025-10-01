<template>
  <div class="user-profile-container">
    <el-card class="profile-card">
      <template #header>
        <div class="card-header">
          <span>个人信息</span>
          <el-button 
            type="primary" 
            @click="handleEditProfile"
            v-if="!isEditing"
          >
            编辑信息
          </el-button>
        </div>
      </template>

      <div v-if="!isEditing">
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
      </div>

      <div v-else>
        <el-form
          ref="profileFormRef"
          :model="profileForm"
          :rules="profileRules"
          label-width="100px"
        >
          <el-form-item label="用户名">
            <el-input v-model="profileForm.username" disabled />
          </el-form-item>
          <el-form-item label="姓名" prop="full_name">
            <el-input v-model="profileForm.full_name" />
          </el-form-item>
          <el-form-item label="邮箱" prop="email">
            <el-input v-model="profileForm.email" type="email" />
          </el-form-item>
          <el-form-item label="手机号" prop="phone">
            <el-input v-model="profileForm.phone" />
          </el-form-item>
          
          <el-form-item>
            <el-button 
              type="primary" 
              @click="saveProfile"
              :loading="loading"
            >
              保存
            </el-button>
            <el-button @click="cancelEdit">取消</el-button>
          </el-form-item>
        </el-form>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useAccountStore } from '@/stores/account.js'
import UserService from '@/api/user.api.js'
import { ElMessage } from 'element-plus'

const authStore = useAccountStore()

const isEditing = ref(false)
const profileFormRef = ref()
const loading = ref(false)
const user = ref({})

const profileForm = reactive({
  username: '',
  full_name: '',
  email: '',
  phone: ''
})

const profileRules = {
  full_name: [
    { required: true, message: '请输入姓名', trigger: 'blur' }
  ],
  email: [
    { required: true, message: '请输入邮箱', trigger: 'blur' },
    { type: 'email', message: '请输入正确的邮箱地址', trigger: 'blur' }
  ],
  phone: [
    { required: false, message: '请输入手机号', trigger: 'blur' }
  ]
}

// 获取当前用户信息
const loadUserProfile = async () => {
  loading.value = true
  try {
    const data = await UserService.getProfile()
    user.value = data
    profileForm.username = user.value.username
    profileForm.full_name = user.value.full_name || ''
    profileForm.email = user.value.email || ''
    profileForm.phone = user.value.phone || ''
  } catch (error) {
    ElMessage.error('获取用户信息失败')
  } finally {
    loading.value = false
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

// 处理编辑信息
const handleEditProfile = () => {
  isEditing.value = true
}

// 保存个人信息
const saveProfile = async () => {
  if (!profileFormRef.value) return

  await profileFormRef.value.validate(async (valid) => {
    if (valid) {
      loading.value = true
      try {
        const userData = {
          full_name: profileForm.full_name,
          email: profileForm.email,
          phone: profileForm.phone
        }

        const data = await UserService.updateProfile(userData)
        user.value = data
        isEditing.value = false
        
        // 更新auth store中的用户信息
        authStore.setUser(data)
        
        ElMessage.success('信息更新成功')
      } catch (error) {
        ElMessage.error(error.message || '更新失败')
      } finally {
        loading.value = false
      }
    }
  })
}

// 取消编辑
const cancelEdit = () => {
  isEditing.value = false
  // 恢复表单数据
  profileForm.full_name = user.value.full_name || ''
  profileForm.email = user.value.email || ''
  profileForm.phone = user.value.phone || ''
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