import { createPinia, setActivePinia } from 'pinia'
import { mount } from '@vue/test-utils'

import DashboardPage from '@/pages/DashboardPage.vue'

describe('DashboardPage', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
  })

  it('renders the scaffold headline and smoke snapshot data', () => {
    const wrapper = mount(DashboardPage, {
      global: {
        plugins: [createPinia()],
      },
    })

    expect(wrapper.text()).toContain('Frontend Smoke Dashboard')
    expect(wrapper.text()).toContain('Vue 3 + PrimeVue v4 scaffold')
    expect(wrapper.text()).toContain('Smoke Snapshot')
    expect(wrapper.get('[data-testid="row-count"]').text()).toBe('3')
  })
})
