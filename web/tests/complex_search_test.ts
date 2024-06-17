import { expect, test } from '@playwright/test';

test('run a complex search', async ({ page }) => {
	await page.goto('/');

	await page.getByTestId('file-dropzone').getByRole('textbox').click();
	await page.getByTestId('file-dropzone').getByRole('textbox').setInputFiles('tests/data/E. coli WT (Patel et al).ftrs');
	await page.getByTestId('MassLibraryUploader').getByRole('button', { name: 'Escherichia coli' }).click();
	await page.getByTestId('MassLibraryUploader').getByRole('option', { name: 'Complex' }).click();

	await page.getByRole('button', { name: 'Advanced Options' }).click();
	await page.getByTestId('modificationSelector').getByRole('option', { name: '3-3 and 4-3 Cross-Linked Multimers (=)' }).click();
	await page.getByTestId('modificationSelector').getByRole('option', { name: '1-3 Cross-Linked Multimers (=)' }).click();
	await page.getByTestId('modificationSelector').getByRole('option', { name: 'Glycosidic Multimers (-)' }).click();
	await page.getByTestId('modificationSelector').getByRole('option', { name: 'Lactyl Multimers (=Lac)' }).click();
	await page.getByTestId('modificationSelector').getByRole('option', { name: 'Anhydro-MurNAc (Anh)' }).click();
	await page.getByTestId('modificationSelector').getByRole('option', { name: 'Deacetylation (-Ac)' }).click();
	await page.getByTestId('modificationSelector').getByRole('option', { name: 'Deacetylation and Anhydro-MurNAc (-Ac, Anh)' }).click();
	await page.getByTestId('modificationSelector').getByRole('option', { name: 'Amidation (Am)' }).click();
	await page.getByTestId('modificationSelector').getByRole('option', { name: 'O-Acetylation (+Ac)' }).click();
	await page.getByTestId('modificationSelector').getByRole('option', { name: 'Potassium Adduct (K+)' }).click();
	await page.getByTestId('modificationSelector').getByRole('option', { name: 'Sodium Adduct (Na+)' }).click();
	await page.getByTestId('modificationSelector').getByRole('option', { name: 'Extra Disaccharide (+gm)' }).click();
	await page.getByTestId('modificationSelector').getByRole('option', { name: 'Lactyl Peptides (Lac)' }).click();
	await page.getByTestId('modificationSelector').getByRole('option', { name: 'Loss of Disaccharide (-gm)' }).click();
	await page.getByTestId('modificationSelector').getByRole('option', { name: 'Loss of GlcNAc (-g)' }).click();

    // Not sure why data-testid="advanced-ppm-tolerance" works for the first two but
    // data-testid="advanced-cleanup-window" and data-testid="advanced-consolidation-ppm" aren't recognised.
    // Have therefore used the higher level 'data-testid' which do work
	await page.getByTestId('advancedModifications').getByRole('spinbutton').first().click();
	await page.getByTestId('advancedModifications').getByRole('spinbutton').first().fill('5');
	await page.getByTestId('advancedModifications').getByRole('spinbutton').nth(1).click();
	await page.getByTestId('advancedModifications').getByRole('spinbutton').nth(1).fill('1');
	await page.getByTestId('advancedModifications').getByRole('spinbutton').nth(2).click();
	await page.getByTestId('advancedModifications').getByRole('spinbutton').nth(2).fill('0.1');

	const downloadPromise = page.waitForEvent('download');
	await page.getByRole('button', { name: 'Run Analysis' }).click();
	const download = await downloadPromise;
	expect(download.suggestedFilename()).toEqual('E. coli WT (Patel et al).csv');
});
