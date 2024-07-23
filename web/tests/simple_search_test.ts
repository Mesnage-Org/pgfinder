import { expect, test } from "@playwright/test";

test("run a simple search", async ({ page }) => {
  await page.goto("/");
  const ms1_search = page.getByTestId("MS1 Search");

  await ms1_search.getByRole("textbox").click();
  await ms1_search
    .getByRole("textbox")
    .setInputFiles("tests/data/E. coli WT (Patel et al).ftrs");
  await ms1_search.getByRole("button", { name: "Escherichia coli" }).click();
  await ms1_search.getByRole("option", { name: "Simple" }).click();

  const downloadPromise = page.waitForEvent("download");
  await ms1_search.getByRole("button", { name: "Run Analysis" }).click();
  const download = await downloadPromise;
  expect(download.suggestedFilename()).toEqual("E. coli WT (Patel et al).csv");
});
