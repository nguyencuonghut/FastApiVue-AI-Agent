<template>
  <AdminLayout section-label="Phase 2 Auth" title="Không có quyền truy cập">
    <section class="forbidden-page">
      <p class="forbidden-page__eyebrow">Permission Guard</p>
      <h2 class="forbidden-page__title">
        Tài khoản hiện tại không có quyền để mở màn hình này.
      </h2>
      <p class="forbidden-page__body">
        UI guard ở frontend chỉ phản ánh quyền do backend trả về trong
        <code>/api/v1/auth/me</code>. Hãy liên hệ quản trị viên nếu cần mở
        thêm permission.
      </p>
      <RouterLink class="forbidden-page__link" to="/">
        Quay về dashboard
      </RouterLink>
    </section>
  </AdminLayout>
</template>

<script setup lang="ts">
import { RouterLink } from 'vue-router'

import AdminLayout from '@/layouts/AdminLayout.vue'
</script>
