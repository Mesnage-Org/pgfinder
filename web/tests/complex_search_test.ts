import { expect, test } from "@playwright/test";

test("run a complex search", async ({ page }) => {
  await page.goto("/");
  const ms1_search = page.getByTestId("MS1 Search");

  await ms1_search.getByRole("textbox").click();
  await ms1_search
    .getByRole("textbox")
    .setInputFiles("tests/data/E. coli WT (Patel et al).ftrs");
  await ms1_search.getByRole("button", { name: "Escherichia coli" }).click();
  await ms1_search.getByRole("option", { name: "Complex" }).click();

  await ms1_search.getByRole("button", { name: "Advanced Options" }).click();
  await ms1_search
    .getByRole("option", { name: "3-3 and 4-3 Cross-Linked Multimers (=)" })
    .click();
  await ms1_search
    .getByRole("option", { name: "1-3 Cross-Linked Multimers (=)" })
    .click();
  await ms1_search
    .getByRole("option", { name: "Glycosidic Multimers (-)" })
    .click();
  await ms1_search
    .getByRole("option", { name: "Lactyl Multimers (=Lac)" })
    .click();
  await ms1_search
    .getByRole("option", { name: "Anhydro-MurNAc (Anh)" })
    .click();
  await ms1_search.getByRole("option", { name: "Deacetylation (-Ac)" }).click();
  await ms1_search
    .getByRole("option", {
      name: "Deacetylation and Anhydro-MurNAc (-Ac, Anh)",
    })
    .click();
  await ms1_search.getByRole("option", { name: "Amidation (Am)" }).click();
  await ms1_search.getByRole("option", { name: "O-Acetylation (+Ac)" }).click();
  await ms1_search
    .getByRole("option", { name: "Potassium Adduct (K+)" })
    .click();
  await ms1_search.getByRole("option", { name: "Sodium Adduct (Na+)" }).click();
  await ms1_search
    .getByRole("option", { name: "Extra Disaccharide (+gm)" })
    .click();
  await ms1_search
    .getByRole("option", { name: "Lactyl Peptides (Lac)" })
    .click();
  await ms1_search
    .getByRole("option", { name: "Loss of Disaccharide (-gm)" })
    .click();
  await ms1_search.getByRole("option", { name: "Loss of GlcNAc (-g)" }).click();

  await ms1_search.getByRole("spinbutton").first().click();
  await ms1_search.getByRole("spinbutton").first().fill("5");
  await ms1_search.getByRole("spinbutton").nth(1).click();
  await ms1_search.getByRole("spinbutton").nth(1).fill("1");
  await ms1_search.getByRole("spinbutton").nth(2).click();
  await ms1_search.getByRole("spinbutton").nth(2).fill("0.1");

  const downloadPromise = page.waitForEvent("download");
  await ms1_search.getByRole("button", { name: "Run Analysis" }).click();
  const download = await downloadPromise;
  expect(download.suggestedFilename()).toEqual("E. coli WT (Patel et al).csv");
});
