<template>
  <section class="health-table">
    <div class="health-table__header">
      <div>
        <p class="health-table__eyebrow">Shared Visual Contract</p>
        <h3 class="health-table__title">Smoke Snapshot</h3>
      </div>
      <Tag severity="contrast" value="DataTable Lazy-ready" />
    </div>

    <DataTable
      :rows="5"
      :value="rows"
      data-key="id"
      paginator
      responsive-layout="scroll"
    >
      <Column field="domain" header="Domain" />
      <Column field="mode" header="Mode" />
      <Column header="Status">
        <template #body="{ data }">
          <Tag :severity="statusSeverity(data.status)" :value="data.status" />
        </template>
      </Column>
      <Column field="note" header="Note" />
    </DataTable>
  </section>
</template>

<script setup lang="ts">
import Column from 'primevue/column'
import DataTable from 'primevue/datatable'
import Tag from 'primevue/tag'

import type { HealthRow } from '@/types/dashboard'

defineProps<{
  rows: HealthRow[]
}>()

const tagSeverityMap = {
  Healthy: 'success',
  Pending: 'warn',
  Planned: 'secondary',
} as const

function statusSeverity(status: HealthRow['status']) {
  return tagSeverityMap[status]
}
</script>

<style src="./HealthSnapshotTable.css"></style>
