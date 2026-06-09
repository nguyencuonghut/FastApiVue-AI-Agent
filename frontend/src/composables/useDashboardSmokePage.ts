import { computed, ref } from 'vue'

import { toTypedSchema } from '@vee-validate/zod'
import { useForm } from 'vee-validate'
import { z } from 'zod'

import { getApiBaseUrl } from '@/api/runtime'
import type {
  HealthRow,
  QuickFilterValues,
  SummaryCard,
} from '@/types/dashboard'

const quickFilterSchema = toTypedSchema(
  z.object({
    keyword: z.string().min(2, 'Nhập ít nhất 2 ký tự để mô phỏng truy vấn.'),
    ownerEmail: z
      .string()
      .email('Nhập email hợp lệ để mô phỏng chủ sở hữu dashboard.'),
  }),
)

const summaryCards: SummaryCard[] = [
  {
    title: 'Frontend Scaffold',
    value: 'Vue 3 + TS',
    detail: 'Vite, Router, Pinia, PrimeVue v4 và token theme đã sẵn sàng.',
    tone: 'success',
  },
  {
    title: 'Integration Target',
    value: '/api/v1',
    detail: 'Frontend đọc base URL từ Vite env để nối với backend FastAPI.',
    tone: 'info',
  },
  {
    title: 'Enterprise Guardrail',
    value: 'Server-driven',
    detail:
      'DataTable demo chỉ giữ state truy vấn, không giữ tập dữ liệu lớn trong store.',
    tone: 'warn',
  },
]

const healthRows: HealthRow[] = [
  {
    id: 1,
    domain: 'API Gateway',
    status: 'Healthy',
    mode: 'GET /api/v1/health',
    note: 'Smoke contract đã được scaffold ở backend.',
  },
  {
    id: 2,
    domain: 'Theme Tokens',
    status: 'Healthy',
    mode: 'Semantic preset',
    note: 'Dark/light mode đi qua shared token layer thay vì hardcode màu tại page.',
  },
  {
    id: 3,
    domain: 'Import/Export UX',
    status: 'Planned',
    mode: 'Async jobs',
    note: 'Phase sau sẽ dùng progress polling thay vì block UI với file nặng.',
  },
]

export function useDashboardSmokePage() {
  const apiBaseUrl = getApiBaseUrl()
  const lastSubmission = ref<QuickFilterValues | null>(null)

  const { defineField, errors, handleSubmit } = useForm<QuickFilterValues>({
    initialValues: {
      keyword: 'health',
      ownerEmail: 'ops@fastapivue.local',
    },
    validationSchema: quickFilterSchema,
  })

  const [keyword, keywordProps] = defineField('keyword')
  const [ownerEmail, ownerEmailProps] = defineField('ownerEmail')

  const submittedSummary = computed(() => {
    if (!lastSubmission.value) {
      return 'Chưa có submit mô phỏng nào.'
    }

    return `Đã mô phỏng filter "${lastSubmission.value.keyword}" cho ${lastSubmission.value.ownerEmail}.`
  })

  const submitQuickFilter = handleSubmit((values) => {
    lastSubmission.value = values
  })

  return {
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
  }
}
