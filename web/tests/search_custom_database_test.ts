import { expect, test } from "@playwright/test";

test("run a search with a custom database", async ({ page }) => {
  await page.goto("/");
  const ms1_search = page.getByTestId("MS1 Search");

  await ms1_search.getByRole("textbox").click();
  await ms1_search
    .getByRole("textbox")
    .setInputFiles("tests/data/E. coli WT (Patel et al).ftrs");

  await ms1_search.locator("label").filter({ hasText: "Custom" }).click();
  await ms1_search.getByTestId("tab-group").getByRole("textbox").click();
  await ms1_search
    .getByTestId("tab-group")
    .getByRole("textbox")
    .setInputFiles("tests/data/glycans.csv");

  const downloadPromise = page.waitForEvent("download");
  await ms1_search.getByRole("button", { name: "Run Analysis" }).click();
  const download = await downloadPromise;
  expect(download.suggestedFilename()).toEqual("E. coli WT (Patel et al).csv");
});
