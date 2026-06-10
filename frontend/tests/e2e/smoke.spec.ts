import { expect, test } from '@playwright/test'

test('redirects anonymous users to the login page', async ({ page }) => {
  await page.goto('/')

  await expect(
    page.getByRole('heading', { name: 'Đăng nhập quản trị' }),
  ).toBeVisible()
  await expect(page.getByText('Phase 2 Auth Foundation')).toBeVisible()
  await expect(page.getByRole('button', { name: 'Đăng nhập' })).toBeVisible()
})
