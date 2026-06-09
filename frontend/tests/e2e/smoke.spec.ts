import { expect, test } from '@playwright/test'

test('renders the frontend smoke dashboard', async ({ page }) => {
  await page.goto('/')

  await expect(
    page.getByRole('heading', { name: 'Frontend Smoke Dashboard' }),
  ).toBeVisible()
  await expect(page.getByText('Vue 3 + PrimeVue v4 scaffold')).toBeVisible()
  await expect(page.getByText('Smoke Snapshot')).toBeVisible()
})
