import { describe, expect, it } from "vitest";
import { getMessage, localize } from "./i18n";

describe("localization", () => {
  it("returns complete bilingual navigation labels", () => {
    expect(getMessage("en", "overview")).toBe("Executive overview");
    expect(getMessage("ar", "overview")).toBe("نظرة عامة تنفيذية");
    expect(getMessage("ar", "synthetic")).toContain("اصطناعية");
  });

  it("selects localized content without mutating it", () => {
    const content = { en: "Software", ar: "البرامج" };
    expect(localize(content, "ar")).toBe("البرامج");
    expect(content.en).toBe("Software");
  });
});
