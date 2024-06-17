import { expect, test } from '@playwright/test';

test('run a search with two datasets', async ({ page }) => {
	await page.goto('/');

	await page.getByTestId('file-dropzone').getByRole('textbox').click();
	await page
        .getByTestId('file-dropzone')
		.getByRole('textbox')
		.setInputFiles([
			'tests/data/C. difficile WT (Bern et al).ftrs',
			'tests/data/E. coli WT (Patel et al).ftrs'
		]);
	await page.getByTestId('MassLibraryUploader').getByRole('button', { name: 'Clostridium difficile' }).click();
	await page.getByTestId('MassLibraryUploader').getByRole('option', { name: 'Non-Redundant' }).click();

	const downloads: string[] = [];
	page.on('download', (download) => downloads.push(download.suggestedFilename()));
	await page.getByRole('button', { name: 'Run Analysis' }).click();
	await page.waitForEvent('download');
	await page.waitForEvent('download');
	expect(downloads).toEqual(['C. difficile WT (Bern et al).csv', 'E. coli WT (Patel et al).csv']);
});
