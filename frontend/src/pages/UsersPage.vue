<template>
  <AdminLayout section-label="Quản trị hệ thống" title="Danh sách tài khoản">
    <div class="users-page">
      <!-- Top Filters and Actions -->
      <section class="users-page__header">
        <div class="users-page__filters">
          <label class="users-page__filter-field">
            <span class="users-page__filter-label">Tìm kiếm email</span>
            <InputText
              v-model="lazyParams.search"
              placeholder="Nhập email..."
              class="users-page__input-search"
              @input="onSearchInput"
            />
          </label>

          <label class="users-page__filter-field">
            <span class="users-page__filter-label">Trạng thái</span>
            <Select
              v-model="lazyParams.status_filter"
              :options="statusFilterOptions"
              option-label="label"
              option-value="value"
              placeholder="Tất cả"
              class="users-page__status-select"
              @change="onFilterChange"
            />
          </label>
        </div>

        <div class="users-page__actions">
          <Button
            v-if="permissionStore.can('users.create')"
            label="Thêm tài khoản"
            icon="pi pi-plus"
            @click="openCreateDialog"
          />
        </div>
      </section>

      <!-- Main Data Table -->
      <div v-if="generalError" class="users-page__general-error">
        <i class="pi pi-exclamation-triangle" aria-hidden="true" />
        <span>{{ generalError }}</span>
      </div>

      <section class="users-page__table-wrapper">
        <DataTable
          :loading="loading"
          :rows="lazyParams.limit"
          :total-records="totalUsers"
          :value="users"
          data-key="id"
          lazy
          paginator
          responsive-layout="scroll"
          @page="onPageChange"
          @sort="onSortChange"
        >
          <Column field="email" header="Email" sortable />
          <Column field="status" header="Trạng thái">
            <template #body="{ data }">
              <Tag
                :severity="statusSeverity(data.status)"
                :value="statusLabel(data.status)"
              />
            </template>
          </Column>
          <Column header="Vai trò">
            <template #body="{ data }">
              <div class="users-page__role-tags">
                <Tag
                  v-for="role in data.roles"
                  :key="role"
                  :value="role"
                  severity="secondary"
                  class="users-page__role-tag"
                />
              </div>
            </template>
          </Column>
          <Column field="last_login_at" header="Đăng nhập cuối" sortable>
            <template #body="{ data }">
              {{ formatDateTime(data.lastLoginAt) }}
            </template>
          </Column>
          <Column header="Thao tác" class="users-page__actions-column">
            <template #body="{ data }">
              <div class="users-page__row-actions">
                <Button
                  v-if="permissionStore.can('users.update')"
                  icon="pi pi-pencil"
                  severity="secondary"
                  text
                  rounded
                  aria-label="Chỉnh sửa"
                  @click="openEditDialog(data)"
                />
                <Button
                  v-if="permissionStore.can('users.delete')"
                  :disabled="data.id === authStore.currentUser?.id"
                  icon="pi pi-trash"
                  severity="danger"
                  text
                  rounded
                  aria-label="Xóa"
                  @click="openDeleteDialog(data)"
                />
              </div>
            </template>
          </Column>
        </DataTable>
      </section>

      <!-- Create User Dialog -->
      <Dialog
        v-model:visible="createDialogVisible"
        header="Thêm tài khoản mới"
        modal
        class="users-page__dialog"
      >
        <form class="users-page__form" @submit.prevent="submitCreate">
          <div v-if="submitError" class="users-page__submit-error">
            {{ submitError }}
          </div>

          <div class="users-page__form-field">
            <label for="create-email" class="users-page__form-label"
              >Email</label
            >
            <InputText
              id="create-email"
              v-model="createEmail"
              v-bind="createEmailProps"
              fluid
              placeholder="username@domain.com"
            />
            <small class="users-page__field-error">{{
              createErrors.email
            }}</small>
          </div>

          <div class="users-page__form-field">
            <label for="create-password" class="users-page__form-label"
              >Mật khẩu</label
            >
            <InputText
              id="create-password"
              v-model="createPassword"
              v-bind="createPasswordProps"
              type="password"
              fluid
              placeholder="Tối thiểu 8 ký tự"
            />
            <small class="users-page__field-error">{{
              createErrors.password
            }}</small>
          </div>

          <div class="users-page__form-field">
            <label for="create-status" class="users-page__form-label"
              >Trạng thái</label
            >
            <Select
              id="create-status"
              v-model="createStatus"
              v-bind="createStatusProps"
              :options="statusOptions"
              option-label="label"
              option-value="value"
              fluid
            />
            <small class="users-page__field-error">{{
              createErrors.status
            }}</small>
          </div>

          <div class="users-page__form-field">
            <label for="create-roles" class="users-page__form-label"
              >Vai trò</label
            >
            <MultiSelect
              id="create-roles"
              v-model="createRoleNames"
              v-bind="createRoleNamesProps"
              :options="roles"
              option-label="name"
              option-value="name"
              placeholder="Chọn vai trò..."
              fluid
              display="chip"
            />
            <small class="users-page__field-error">{{
              createErrors.roleNames
            }}</small>
          </div>

          <div class="users-page__dialog-actions">
            <Button
              label="Hủy"
              severity="secondary"
              text
              @click="createDialogVisible = false"
            />
            <Button
              :loading="createFormSubmitting"
              label="Lưu tài khoản"
              type="submit"
            />
          </div>
        </form>
      </Dialog>

      <!-- Edit User Dialog -->
      <Dialog
        v-model:visible="editDialogVisible"
        header="Chỉnh sửa tài khoản"
        modal
        class="users-page__dialog"
      >
        <form class="users-page__form" @submit.prevent="submitEdit">
          <div v-if="submitError" class="users-page__submit-error">
            {{ submitError }}
          </div>

          <div class="users-page__form-field">
            <label for="edit-email" class="users-page__form-label">Email</label>
            <InputText
              id="edit-email"
              v-model="editEmail"
              v-bind="editEmailProps"
              fluid
              placeholder="username@domain.com"
            />
            <small class="users-page__field-error">{{
              editErrors.email
            }}</small>
          </div>

          <div class="users-page__form-field">
            <label for="edit-password" class="users-page__form-label">
              Mật khẩu mới (bỏ trống nếu không đổi)
            </label>
            <InputText
              id="edit-password"
              v-model="editPassword"
              v-bind="editPasswordProps"
              type="password"
              fluid
              placeholder="Tối thiểu 8 ký tự"
            />
            <small class="users-page__field-error">{{
              editErrors.password
            }}</small>
          </div>

          <div class="users-page__form-field">
            <label for="edit-status" class="users-page__form-label"
              >Trạng thái</label
            >
            <Select
              id="edit-status"
              v-model="editStatus"
              v-bind="editStatusProps"
              :options="statusOptions"
              option-label="label"
              option-value="value"
              fluid
            />
            <small class="users-page__field-error">{{
              editErrors.status
            }}</small>
          </div>

          <div class="users-page__form-field">
            <label for="edit-roles" class="users-page__form-label"
              >Vai trò</label
            >
            <MultiSelect
              id="edit-roles"
              v-model="editRoleNames"
              v-bind="editRoleNamesProps"
              :options="roles"
              option-label="name"
              option-value="name"
              placeholder="Chọn vai trò..."
              fluid
              display="chip"
            />
            <small class="users-page__field-error">{{
              editErrors.roleNames
            }}</small>
          </div>

          <div class="users-page__dialog-actions">
            <Button
              label="Hủy"
              severity="secondary"
              text
              @click="editDialogVisible = false"
            />
            <Button
              :loading="editFormSubmitting"
              label="Cập nhật"
              type="submit"
            />
          </div>
        </form>
      </Dialog>

      <!-- Delete User Dialog -->
      <Dialog
        v-model:visible="deleteDialogVisible"
        header="Xác nhận xóa tài khoản"
        modal
        class="users-page__dialog"
      >
        <div class="users-page__delete-confirm">
          <i
            class="pi pi-exclamation-triangle users-page__delete-icon"
            aria-hidden="true"
          />
          <p>
            Bạn có chắc chắn muốn xóa vĩnh viễn tài khoản
            <strong>{{ selectedUser?.email }}</strong
            >? Thao tác này không thể hoàn tác.
          </p>
        </div>

        <div v-if="submitError" class="users-page__submit-error">
          {{ submitError }}
        </div>

        <div class="users-page__dialog-actions">
          <Button
            label="Hủy"
            severity="secondary"
            text
            @click="deleteDialogVisible = false"
          />
          <Button
            :loading="isDeleting"
            label="Xóa tài khoản"
            severity="danger"
            @click="submitDelete"
          />
        </div>
      </Dialog>
    </div>
  </AdminLayout>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import Button from 'primevue/button'
import Column from 'primevue/column'
import DataTable from 'primevue/datatable'
import Dialog from 'primevue/dialog'
import InputText from 'primevue/inputtext'
import MultiSelect from 'primevue/multiselect'
import Select from 'primevue/select'
import Tag from 'primevue/tag'

import { useUsersPage } from '@/composables/useUsersPage'
import AdminLayout from '@/layouts/AdminLayout.vue'
import { useAuthStore } from '@/stores/auth.store'
import { usePermissionStore } from '@/stores/permission.store'

const authStore = useAuthStore()
const permissionStore = usePermissionStore()

const {
  users,
  totalUsers,
  loading,
  roles,
  lazyParams,
  generalError,
  submitError,
  createDialogVisible,
  editDialogVisible,
  deleteDialogVisible,
  selectedUser,
  isDeleting,
  fetchUsers,
  fetchRoles,
  openCreateDialog,
  openEditDialog,
  openDeleteDialog,
  submitDelete,
  createEmail,
  createEmailProps,
  createPassword,
  createPasswordProps,
  createStatus,
  createStatusProps,
  createRoleNames,
  createRoleNamesProps,
  createErrors,
  submitCreate,
  createFormSubmitting,
  editEmail,
  editEmailProps,
  editPassword,
  editPasswordProps,
  editStatus,
  editStatusProps,
  editRoleNames,
  editRoleNamesProps,
  editErrors,
  submitEdit,
  editFormSubmitting,
} = useUsersPage()

const statusOptions = [
  { label: 'Đang hoạt động', value: 'active' },
  { label: 'Tạm ngưng', value: 'inactive' },
  { label: 'Bị khóa', value: 'locked' },
]

const statusFilterOptions = [
  { label: 'Tất cả', value: '' },
  { label: 'Đang hoạt động', value: 'active' },
  { label: 'Tạm ngưng', value: 'inactive' },
  { label: 'Bị khóa', value: 'locked' },
]

const statusSeverityMap = {
  active: 'success',
  inactive: 'warn',
  locked: 'danger',
} as const

const statusLabelMap = {
  active: 'Đang hoạt động',
  inactive: 'Tạm ngưng',
  locked: 'Bị khóa',
} as const

function statusSeverity(statusVal: string) {
  return (
    statusSeverityMap[statusVal as keyof typeof statusSeverityMap] ||
    'secondary'
  )
}

function statusLabel(statusVal: string) {
  return statusLabelMap[statusVal as keyof typeof statusLabelMap] || statusVal
}

// Debounced search
let searchTimeout: ReturnType<typeof window.setTimeout> | null = null
function onSearchInput() {
  if (searchTimeout) {
    window.clearTimeout(searchTimeout)
  }
  searchTimeout = window.setTimeout(() => {
    lazyParams.offset = 0
    fetchUsers()
  }, 400)
}

function onFilterChange() {
  lazyParams.offset = 0
  fetchUsers()
}

function onPageChange(event: { first: number; rows: number }) {
  lazyParams.offset = event.first
  lazyParams.limit = event.rows
  fetchUsers()
}

function onSortChange(event: {
  sortField?: string | ((item: unknown) => string)
  sortOrder?: number | null
}) {
  const sortField =
    typeof event.sortField === 'string' ? event.sortField : undefined
  lazyParams.sort_by = sortField || 'created_at'
  lazyParams.sort_order = event.sortOrder === 1 ? 'asc' : 'desc'
  lazyParams.offset = 0
  fetchUsers()
}

function formatDateTime(val: string | null) {
  if (!val) return 'Chưa từng đăng nhập'
  try {
    const tz = import.meta.env.VITE_APP_TIMEZONE ?? 'Asia/Ho_Chi_Minh'
    return new Intl.DateTimeFormat('vi-VN', {
      dateStyle: 'medium',
      timeStyle: 'short',
      timeZone: tz,
    }).format(new Date(val))
  } catch {
    return val
  }
}

onMounted(async () => {
  await Promise.all([fetchUsers(), fetchRoles()])
})
</script>
