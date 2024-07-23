import { expect, test } from "@playwright/test";

test("run a search with two datasets", async ({ page }) => {
  await page.goto("/");
  const ms1_search = page.getByTestId("MS1 Search");

  await ms1_search.getByRole("textbox").click();
  await ms1_search
    .getByRole("textbox")
    .setInputFiles([
      "tests/data/C. difficile WT (Bern et al).ftrs",
      "tests/data/E. coli WT (Patel et al).ftrs",
    ]);
  await ms1_search
    .getByRole("button", { name: "Clostridium difficile" })
    .click();
  await ms1_search.getByRole("option", { name: "Non-Redundant" }).click();

  const downloads: string[] = [];
  page.on("download", (download) =>
    downloads.push(download.suggestedFilename()),
  );
  await ms1_search.getByRole("button", { name: "Run Analysis" }).click();
  await page.waitForEvent("download");
  await page.waitForEvent("download");
  expect(downloads).toEqual([
    "C. difficile WT (Bern et al).csv",
    "E. coli WT (Patel et al).csv",
  ]);
});
