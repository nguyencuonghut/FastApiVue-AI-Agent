<template>
  <Card class="quick-filter">
    <template #title>
      <div class="quick-filter__title-row">
        <div>
          <p class="quick-filter__eyebrow">Validation Scaffold</p>
          <h3 class="quick-filter__title">Quick Filter Form</h3>
        </div>
        <Button form="quick-filter-form" label="Submit" type="submit" />
      </div>
    </template>

    <template #content>
      <form
        id="quick-filter-form"
        class="quick-filter__form"
        @submit.prevent="onSubmit"
      >
        <label class="quick-filter__field">
          <span class="quick-filter__field-label">Keyword</span>
          <InputText
            v-model="keywordModel"
            v-bind="keywordProps"
            placeholder="health, import, dashboard"
          />
          <small class="quick-filter__error">{{ errors.keyword }}</small>
        </label>

        <label class="quick-filter__field">
          <span class="quick-filter__field-label">Owner Email</span>
          <InputText
            v-model="ownerEmailModel"
            v-bind="ownerEmailProps"
            placeholder="ops@fastapivue.local"
          />
          <small class="quick-filter__error">{{ errors.ownerEmail }}</small>
        </label>
      </form>

      <div class="quick-filter__footer">
        <Tag :value="apiBaseUrl" severity="info" />
        <p class="quick-filter__summary">{{ submittedSummary }}</p>
      </div>
    </template>
  </Card>
</template>

<script setup lang="ts">
import Button from 'primevue/button'
import Card from 'primevue/card'
import InputText from 'primevue/inputtext'
import Tag from 'primevue/tag'

defineProps<{
  apiBaseUrl: string
  errors: Record<string, string | undefined>
  keywordProps: Record<string, unknown>
  ownerEmailProps: Record<string, unknown>
  submittedSummary: string
}>()

const emit = defineEmits<{
  submit: []
}>()

const keywordModel = defineModel<string>('keyword', { required: true })
const ownerEmailModel = defineModel<string>('ownerEmail', { required: true })

function onSubmit() {
  emit('submit')
}
</script>

<style src="./QuickFilterForm.css"></style>
