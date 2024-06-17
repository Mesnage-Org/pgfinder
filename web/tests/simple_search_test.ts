import { expect, test } from '@playwright/test';

test('run a simple search', async ({ page }) => {
	await page.goto('/');

	await page.getByTestId('file-dropzone').getByRole('textbox').click();
	await page.getByTestId('file-dropzone').getByRole('textbox').setInputFiles('tests/data/E. coli WT (Patel et al).ftrs');
	await page.getByTestId('MassLibraryUploader').getByRole('button', { name: 'Escherichia coli' }).click();
	await page.getByTestId('MassLibraryUploader').getByRole('option', { name: 'Simple' }).click();

	const downloadPromise = page.waitForEvent('download');
	await page.getByTestId('PGFinder').getByRole('button', { name: 'Run Analysis' }).click();
	const download = await downloadPromise;
	expect(download.suggestedFilename()).toEqual('E. coli WT (Patel et al).csv');
});
