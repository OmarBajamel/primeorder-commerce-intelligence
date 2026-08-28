import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, expect, it } from "vitest";
import { KpiCard, StatusChip } from "./ui";

describe("dashboard UI primitives", () => {
  it("exposes KPI definitions to keyboard and assistive technology", async () => {
    const user = userEvent.setup();
    render(<KpiCard label="Net revenue" value="SAR 12,000" formula="Gross revenue minus refunds" />);
    const trigger = screen.getByRole("button", { name: "Gross revenue minus refunds" });
    await user.tab();
    expect(trigger).toHaveFocus();
    expect(screen.getByRole("tooltip")).toHaveTextContent("Gross revenue minus refunds");
  });

  it("renders machine statuses as readable chips", () => {
    render(<StatusChip status="READY_NOT_AUTHENTICATED" />);
    expect(screen.getByText("READY NOT AUTHENTICATED")).toBeVisible();
  });
});
