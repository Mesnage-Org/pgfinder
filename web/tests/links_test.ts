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
    .getByRole("link", { name: "https://doi.org/10.7554/eLife.70597" })
    .click();
  const page4 = await page4Promise;
  // NOTE: Cloudflare blocks us from loading the page, so the best we can do is check the URL...
  await page4.waitForLoadState("domcontentloaded");
  expect(page4.url()).toEqual("https://elifesciences.org/articles/70597");

  await page.getByTestId("drawer-backdrop").click();

  const page5Promise = page.waitForEvent("popup");
  await page.getByRole("link").first().click();
  const page5 = await page5Promise;
  await page5.waitForLoadState("domcontentloaded");
  const title = await page5.title();
  expect(title).toContain("Usage");
  expect(title).toContain("documentation");

  const page6Promise = page.waitForEvent("popup");
  await page.getByRole("link").nth(1).click();
  const page6 = await page6Promise;
  await page6.waitForLoadState("domcontentloaded");
  expect(await page6.title()).toEqual(
    "GitHub - Mesnage-Org/pgfinder: Peptidoglycan MS1 Analysis Tool",
  );
});
