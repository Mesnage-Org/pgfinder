import { expect, test } from "@playwright/test";

test("links are live", async ({ page }) => {
  test.slow();
  await page.goto("/");
  await page.locator("#shell-header").getByRole("button").click();

  const page1Promise = page.waitForEvent("popup");
  await page
    .getByRole("link", { name: "Browse Built-In Mass Databases" })
    .click();
  const page1 = await page1Promise;
  await page1.waitForLoadState("domcontentloaded");
  expect(await page1.title()).toEqual(
    "pgfinder/lib/pgfinder/masses at master · Mesnage-Org/pgfinder · GitHub",
  );

  const page2Promise = page.waitForEvent("popup");
  await page.getByRole("link", { name: "Download MaxQuant" }).click();
  const page2 = await page2Promise;
  await page2.waitForLoadState("domcontentloaded");
  expect(await page2.title()).toEqual("MaxQuant");

  const page3Promise = page.waitForEvent("popup");
  await page
    .getByRole("link", { name: "Download ProteoWizard (MSConvert)" })
    .click();
  const page3 = await page3Promise;
  await page3.waitForLoadState("domcontentloaded");
  expect(await page3.title()).toEqual("ProteoWizard: Download");

  const page4Promise = page.waitForEvent("popup");
  await page
    .getByRole("link", { name: "Glycopeptide Database Builder (GLAM)" })
    .click();
  const page4 = await page4Promise;
  await page4.waitForLoadState("domcontentloaded");
  expect(await page4.title()).toEqual("GLAM");

  const page5Promise = page.waitForEvent("popup");
  await page
    .getByRole("link", { name: "https://doi.org/10.1038/s42004-025-01490-6" })
    .click();
  const page5 = await page5Promise;
  await page5.waitForLoadState("domcontentloaded");
  expect(await page5.title()).toEqual(
    "A software tool and strategy for peptidoglycomics, the high-resolution analysis of bacterial peptidoglycans via LC-MS/MS | Communications Chemistry",
  );

  const page6Promise = page.waitForEvent("popup");
  await page
    .getByRole("link", { name: "https://doi.org/10.7554/eLife.70597" })
    .click();
  const page6 = await page6Promise;
  await page6.waitForLoadState("domcontentloaded");
  expect(await page6.title()).toEqual(
    "PGFinder, a novel analysis pipeline for the consistent, reproducible, and high-resolution structural analysis of bacterial peptidoglycans | eLife",
  );

  const page7Promise = page.waitForEvent("popup");
  await page
    .getByRole("link", { name: "https://doi.org/10.1007/978-1-0716-4007-4_8" })
    .click();
  const page7 = await page7Promise;
  await page7.waitForLoadState("domcontentloaded");
  expect(await page7.title()).toEqual(
    "PGFinder, an Open-Source Software for Peptidoglycomics: The Structural Analysis of Bacterial Peptidoglycan by LC-MS | SpringerLink",
  );

  await page.getByTestId("drawer-backdrop").click();

  const page8Promise = page.waitForEvent("popup");
  await page.getByRole("link").first().click();
  const page8 = await page8Promise;
  await page8.waitForLoadState("domcontentloaded");
  const title = await page8.title();
  expect(title).toContain("Usage");
  expect(title).toContain("documentation");

  const page9Promise = page.waitForEvent("popup");
  await page.getByRole("link").nth(1).click();
  const page9 = await page9Promise;
  await page9.waitForLoadState("domcontentloaded");
  expect(await page9.title()).toEqual(
    "GitHub - Mesnage-Org/pgfinder: Peptidoglycan MS1 Analysis Tool",
  );
});
