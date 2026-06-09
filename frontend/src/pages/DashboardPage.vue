<template>
  <AdminLayout title="Frontend Smoke Dashboard">
    <div class="dashboard-page">
      <section class="dashboard-page__hero">
        <div>
          <p class="dashboard-page__eyebrow">Admin UI Baseline</p>
          <h2 class="dashboard-page__headline">
            Vue 3 + PrimeVue v4 scaffold với dark/light mode đồng nhất.
          </h2>
          <p class="dashboard-page__lead">
            Layout, token theme, DataTable demo, Router, Pinia và validation đã
            được scaffold để làm nền cho dashboard enterprise.
          </p>
        </div>
        <Tag severity="success" value="Phase 1 / Step 3" />
      </section>

      <SummaryCards :cards="summaryCards" />

      <section class="dashboard-page__body">
        <QuickFilterForm
          v-model:keyword="keyword"
          v-model:owner-email="ownerEmail"
          :api-base-url="apiBaseUrl"
          :errors="errors"
          :keyword-props="keywordProps"
          :owner-email-props="ownerEmailProps"
          :submitted-summary="submittedSummary"
          @submit="submitQuickFilter"
        />
        <HealthSnapshotTable :rows="healthRows" />
      </section>
    </div>
  </AdminLayout>
</template>

<script setup lang="ts">
import Tag from 'primevue/tag'

import HealthSnapshotTable from '@/components/dashboard/HealthSnapshotTable.vue'
import QuickFilterForm from '@/components/dashboard/QuickFilterForm.vue'
import SummaryCards from '@/components/dashboard/SummaryCards.vue'
import { useDashboardSmokePage } from '@/composables/useDashboardSmokePage'
import AdminLayout from '@/layouts/AdminLayout.vue'

const {
  apiBaseUrl,
  errors,
  healthRows,
  keyword,
  keywordProps,
  ownerEmail,
  ownerEmailProps,
  submitQuickFilter,
  submittedSummary,
  summaryCards,
} = useDashboardSmokePage()
</script>

<style src="./DashboardPage.css"></style>
