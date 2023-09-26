import { expect, test } from '@playwright/test';

test('run a search with a custom database', async ({ page }) => {
	await page.goto('/');

	await page.getByRole('textbox').click();
	await page.getByRole('textbox').setInputFiles('tests/data/E. coli WT (Patel et al).ftrs');

	await page.locator('label').filter({ hasText: 'Custom' }).click();
	await page.getByTestId('tab-group').getByRole('textbox').click();
	await page.getByTestId('tab-group').getByRole('textbox').setInputFiles('tests/data/glycans.csv');

	const downloadPromise = page.waitForEvent('download');
	await page.getByRole('button', { name: 'Run Analysis' }).click();
	const download = await downloadPromise;
	expect(download.suggestedFilename()).toEqual('E. coli WT (Patel et al).csv');
});
