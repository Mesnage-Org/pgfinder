import { expect, test } from '@playwright/test';

test('links are live', async ({ page }) => {
	test.slow();
	await page.goto('/');
	await page.locator('#shell-header').getByRole('button').click();

	const page1Promise = page.waitForEvent('popup');
	await page.getByRole('link', { name: 'Browse Built-In Mass Databases' }).click();
	const page1 = await page1Promise;
	await page1.waitForLoadState('domcontentloaded');
	expect(await page1.title()).toEqual(
		'pgfinder/pgfinder/masses at master · Mesnage-Org/pgfinder · GitHub'
	);

	const page2Promise = page.waitForEvent('popup');
	await page.getByRole('link', { name: 'Download MaxQuant' }).click();
	const page2 = await page2Promise;
	await page2.waitForLoadState('domcontentloaded');
	expect(await page2.title()).toEqual('MaxQuant');

	const page3Promise = page.waitForEvent('popup');
	await page.getByRole('link', { name: 'Download ProteoWizard (MSConvert)' }).click();
	const page3 = await page3Promise;
	await page3.waitForLoadState('domcontentloaded');
	expect(await page3.title()).toEqual('ProteoWizard: Download');

	const page4Promise = page.waitForEvent('popup');
	await page.getByRole('link', { name: 'https://doi.org/10.7554/eLife.70597' }).click();
	const page4 = await page4Promise;
	// NOTE: Cloudflare blocks us from loading the page, so the best we can do is check the URL...
	await page4.waitForLoadState('domcontentloaded');
	expect(page4.url()).toEqual('https://elifesciences.org/articles/70597');

	await page.getByTestId('drawer-backdrop').click();

	const page5Promise = page.waitForEvent('popup');
	await page.getByRole('link').first().click();
	const page5 = await page5Promise;
	await page5.waitForLoadState('domcontentloaded');
	expect(await page5.title()).toEqual('Usage — pgFinder 1.0.3.dev9+g56a3739 documentation');

	const page6Promise = page.waitForEvent('popup');
	await page.getByRole('link').nth(1).click();
	const page6 = await page6Promise;
	await page6.waitForLoadState('domcontentloaded');
	expect(await page6.title()).toEqual(
		'GitHub - Mesnage-Org/pgfinder: Peptidoglycan MS1 Analysis Tool'
	);
});

test('example data can be downloaded', async ({ page }) => {
	await page.goto('/');
	await page.locator('#shell-header').getByRole('button').click();

	const downloadPromise = page.waitForEvent('download');
	await page
		.getByRole('link', { name: 'Escherichia coli Strain BW25113 — Patel et al. 2021' })
		.click();
	const download = await downloadPromise;
	expect(download.suggestedFilename()).toEqual('E. coli WT (Patel et al).ftrs');

	const download1Promise = page.waitForEvent('download');
	await page
		.getByRole('link', { name: 'Clostridium difficile Strain R20291 — Bern et al. 2017' })
		.click();
	const download1 = await download1Promise;
	expect(download1.suggestedFilename()).toEqual('C. difficile WT (Bern et al).ftrs');
});

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

test('run a search with two datasets', async ({ page }) => {
	await page.goto('/');

	await page.getByRole('textbox').click();
	await page
		.getByRole('textbox')
		.setInputFiles([
			'tests/data/C. difficile WT (Bern et al).ftrs',
			'tests/data/E. coli WT (Patel et al).ftrs'
		]);
	await page.getByRole('button', { name: 'Clostridium difficile' }).click();
	await page.getByRole('option', { name: 'Non-Redundant' }).click();

	const downloads: string[] = [];
	page.on('download', (download) => downloads.push(download.suggestedFilename()));
	await page.getByRole('button', { name: 'Run Analysis' }).click();
	await page.waitForEvent('download');
	await page.waitForEvent('download');
	expect(downloads).toEqual(['C. difficile WT (Bern et al).csv', 'E. coli WT (Patel et al).csv']);
});

test('run a complex search', async ({ page }) => {
	await page.goto('/');

	await page.getByRole('textbox').click();
	await page.getByRole('textbox').setInputFiles('tests/data/E. coli WT (Patel et al).ftrs');
	await page.getByRole('button', { name: 'Escherichia coli' }).click();
	await page.getByRole('option', { name: 'Complex' }).click();

	await page.getByRole('button', { name: 'Advanced Options' }).click();
	await page.getByRole('option', { name: 'Cross-Linked Multimers (=)' }).click();
	await page.getByRole('option', { name: 'Glycosidic Multimers (-)' }).click();
	await page.getByRole('option', { name: 'Lactyl Multimers (=Lac)' }).click();
	await page.getByRole('option', { name: 'Anhydro-MurNAc (Anh)' }).click();
	await page.getByRole('option', { name: 'Deacetylation (-Ac)' }).click();
	await page.getByRole('option', { name: 'Deacetylation and Anhydro-MurNAc (-Ac, Anh)' }).click();
	await page.getByRole('option', { name: 'Amidation (Am)' }).click();
	await page.getByRole('option', { name: 'O-Acetylation (+Ac)' }).click();
	await page.getByRole('option', { name: 'Potassium Adduct (K+)' }).click();
	await page.getByRole('option', { name: 'Sodium Adduct (Na+)' }).click();
	await page.getByRole('option', { name: 'Extra Disaccharide (+gm)' }).click();
	await page.getByRole('option', { name: 'Lactyl Peptides (Lac)' }).click();
	await page.getByRole('option', { name: 'Loss of Disaccharide (-gm)' }).click();
	await page.getByRole('option', { name: 'Loss of GlcNAc (-g)' }).click();

	await page.getByRole('spinbutton').first().click();
	await page.getByRole('spinbutton').first().fill('5');
	await page.getByRole('spinbutton').nth(1).click();
	await page.getByRole('spinbutton').nth(1).fill('1');
	await page.getByRole('spinbutton').nth(2).click();
	await page.getByRole('spinbutton').nth(2).fill('0.1');

	const downloadPromise = page.waitForEvent('download');
	await page.getByRole('button', { name: 'Run Analysis' }).click();
	const download = await downloadPromise;
	expect(download.suggestedFilename()).toEqual('E. coli WT (Patel et al).csv');
});

test('run a search with a custom library', async ({ page }) => {
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
