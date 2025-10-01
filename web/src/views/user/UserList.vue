<template>
  <AppHeader />
  <div class="container py-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h4>用户管理</h4>
      <button class="btn btn-primary" @click="goToCreateUser">
        <i class="bi bi-plus-circle"></i> 创建用户
      </button>
    </div>

    <div class="card">
      <div class="card-body">
        <div class="table-responsive">
          <table class="table table-striped table-hover">
            <thead>
            <tr>
              <th>ID</th>
              <th>用户名</th>
              <th>姓名</th>
              <th>邮箱</th>
              <th>手机号</th>
              <th>用户类型</th>
              <th>状态</th>
              <th>操作</th>
            </tr>
            </thead>
            <tbody>
            <tr v-for="user in users" :key="user.id">
              <td>{{ user.id }}</td>
              <td>{{ user.username }}</td>
              <td>{{ user.full_name }}</td>
              <td>{{ user.email }}</td>
              <td>{{ user.phone }}</td>
              <td>
                  <span :class="getUserTypeClass(user)">
                    {{ getUserTypeText(user) }}
                  </span>
              </td>
              <td>
                  <span :class="getStatusClass(user)">
                    {{ user.is_active ? '激活' : '未激活' }}
                  </span>
              </td>
              <td>
                <button class="btn btn-sm btn-outline-primary me-1" @click="viewUser(user.id)">
                  查看
                </button>
                <button class="btn btn-sm btn-outline-secondary me-1" @click="editUser(user)">
                  编辑
                </button>
                <button class="btn btn-sm btn-outline-danger" @click="deleteUser(user)" :disabled="user.id === currentUser.id">
                  删除
                </button>
              </td>
            </tr>
            <tr v-if="users.length === 0">
              <td colspan="8" class="text-center">暂无用户数据</td>
            </tr>
            </tbody>
          </table>
        </div>

        <div class="d-flex justify-content-between align-items-center mt-3">
          <div>
            显示第 {{ (currentPage - 1) * pageSize + 1 }} 到 {{ Math.min(currentPage * pageSize, total) }} 条记录，
            总共 {{ total }} 条记录
          </div>
          <nav>
            <ul class="pagination mb-0">
              <li class="page-item" :class="{ disabled: currentPage === 1 }">
                <a class="page-link" href="#" @click.prevent="changePage(currentPage - 1)">上一页</a>
              </li>
              <li class="page-item" v-for="page in totalPages" :key="page" :class="{ active: page === currentPage }">
                <a class="page-link" href="#" @click.prevent="changePage(page)">{{ page }}</a>
              </li>
              <li class="page-item" :class="{ disabled: currentPage === totalPages }">
                <a class="page-link" href="#" @click.prevent="changePage(currentPage + 1)">下一页</a>
              </li>
            </ul>
          </nav>
        </div>
      </div>
    </div>
  </div>
  <AppFooter />
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import UserService from '@/api/user.api.js'
import { useAccountStore } from '@/stores/account.js'
import AppHeader from '@/components/layout/AppHeader.vue'
import AppFooter from '@/components/layout/AppFooter.vue'

// 获取路由实例
const router = useRouter()
const accountStore = useAccountStore()
const currentUser = computed(() => accountStore.user)

// 定义响应式数据
const users = ref([])
const loading = ref(false)
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)

// 计算总页数
const totalPages = computed(() => {
  return Math.ceil(total.value / pageSize.value)
})

// 获取用户列表
const loadUsers = async (page = 1) => {
  loading.value = true
  try {
    const params = {
      page: page,
      page_size: pageSize.value
    }
    // 这里假设后端API支持分页，如果需要搜索功能也可以添加相关参数
    const response = await UserService.getUsers(params)

    // 根据实际API响应结构调整
    if (response.results) {
      users.value = response.results
      total.value = response.count || response.results.length
    } else {
      users.value = response
      total.value = response.length
    }

    currentPage.value = page
  } catch (error) {
    console.error('获取用户列表失败:', error)
    ElMessage.error(error.response?.data?.detail || error.message || '获取用户列表失败')
  } finally {
    loading.value = false
  }
}

// 查看用户详情
const viewUser = (userId) => {
  router.push(`/users/${userId}`)
}

// 编辑用户
const editUser = (user) => {
  router.push(`/users/${user.id}/edit`)
}

// 删除用户
const deleteUser = (user) => {
  ElMessageBox.confirm(
      `确定要删除用户 "${user.username}" 吗？此操作不可恢复！`,
      '确认删除',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
      }
  ).then(async () => {
    try {
      await UserService.deleteUser(user.id)
      ElMessage.success('用户删除成功')
      // 重新加载用户列表
      loadUsers(currentPage.value)
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

// 获取用户类型CSS类
const getUserTypeClass = (user) => {
  if (user.is_superuser) return 'badge bg-danger'
  if (user.is_staff) return 'badge bg-warning'
  return 'badge bg-info'
}

// 获取状态CSS类
const getStatusClass = (user) => {
  return user.is_active ? 'badge bg-success' : 'badge bg-secondary'
}

// 跳转到创建用户页面
const goToCreateUser = () => {
  router.push('/users/create')
}

// 更改页面
const changePage = (page) => {
  if (page >= 1 && page <= totalPages.value) {
    loadUsers(page)
  }
}

// 组件挂载时加载数据
onMounted(() => {
  loadUsers()
})
</script>

<style scoped>
.table th {
  font-weight: 600;
}

.badge {
  font-size: 0.75em;
}

.pagination {
  margin-bottom: 0;
}

.btn-sm {
  padding: 0.25rem 0.5rem;
  font-size: 0.875rem;
}
</style>
