import { expect, test } from "@playwright/test";

test("example data can be downloaded", async ({ page }) => {
  await page.goto("/");
  await page.locator("#shell-header").getByRole("button").click();

  const downloadPromise = page.waitForEvent("download");
  await page
    .getByRole("link", {
      name: "Escherichia coli Strain BW25113 — Patel et al. 2021",
    })
    .click();
  const download = await downloadPromise;
  expect(download.suggestedFilename()).toEqual("E. coli WT (Patel et al).ftrs");

  const download1Promise = page.waitForEvent("download");
  await page
    .getByRole("link", {
      name: "Clostridium difficile Strain R20291 — Bern et al. 2017",
    })
    .click();
  const download1 = await download1Promise;
  expect(download1.suggestedFilename()).toEqual(
    "C. difficile WT (Bern et al).ftrs",
  );
});
