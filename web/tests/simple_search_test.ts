import { expect, test } from '@playwright/test';

test('run a simple search', async ({ page }) => {
	await page.goto('/');

	await page.getByRole('textbox').click();
	await page.getByRole('textbox').setInputFiles('tests/data/E. coli WT (Patel et al).ftrs');
	await page.getByRole('button', { name: 'Escherichia coli' }).click();
	await page.getByRole('option', { name: 'Simple' }).click();

	const downloadPromise = page.waitForEvent('download');
	await page.getByRole('button', { name: 'Run Analysis' }).click();
	const download = await downloadPromise;
	expect(download.suggestedFilename()).toEqual('E. coli WT (Patel et al).csv');
});
