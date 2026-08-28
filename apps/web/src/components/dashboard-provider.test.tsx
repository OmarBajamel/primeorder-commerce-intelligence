import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { DashboardProvider, useDashboard } from "./dashboard-provider";

function Probe() {
  const { locale, setLocale, state, filteredRecords } = useDashboard();
  return <><button onClick={() => setLocale(locale === "en" ? "ar" : "en")}>switch</button><span data-testid="locale">{locale}</span><span data-testid="state">{state}</span><span data-testid="count">{filteredRecords.length}</span></>;
}

describe("DashboardProvider", () => {
  beforeEach(() => {
    window.localStorage.clear();
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue({ ok: true, json: async () => ({ schemaVersion: "1.0", meta: { dataMode: "public-demo", seed: 20250301 } }) }));
  });
  afterEach(() => vi.unstubAllGlobals());

  it("loads a safe public dataset and switches the document to Arabic RTL", async () => {
    const user = userEvent.setup();
    render(<DashboardProvider><Probe /></DashboardProvider>);
    await waitFor(() => expect(screen.getByTestId("state")).toHaveTextContent("ready"));
    expect(Number(screen.getByTestId("count").textContent)).toBeGreaterThan(0);
    await user.click(screen.getByRole("button", { name: "switch" }));
    expect(screen.getByTestId("locale")).toHaveTextContent("ar");
    expect(document.documentElement).toHaveAttribute("dir", "rtl");
    expect(document.documentElement).toHaveAttribute("lang", "ar");
  });

  it("uses the deterministic fallback when static JSON fails", async () => {
    vi.stubGlobal("fetch", vi.fn().mockRejectedValue(new Error("offline")));
    render(<DashboardProvider><Probe /></DashboardProvider>);
    await waitFor(() => expect(screen.getByTestId("state")).toHaveTextContent("fallback"));
    expect(Number(screen.getByTestId("count").textContent)).toBeGreaterThan(0);
  });
});
