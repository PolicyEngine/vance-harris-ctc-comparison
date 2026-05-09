import { describe, it, expect, vi } from "vitest";
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { MantineProvider } from "@mantine/core";
import HouseholdForm from "../components/HouseholdForm";

function renderForm(overrides = {}) {
  const defaults = {
    isMarried: false,
    setIsMarried: vi.fn(),
    numChildren: 1,
    setNumChildren: vi.fn(),
    childAges: [5],
    setChildAges: vi.fn(),
    earnings: 50000,
    setEarnings: vi.fn(),
    onCalculate: vi.fn(),
    loading: false,
    ...overrides,
  };
  return render(
    <MantineProvider>
      <HouseholdForm {...defaults} />
    </MantineProvider>,
  );
}

describe("HouseholdForm", () => {
  it("renders married checkbox", () => {
    renderForm();
    expect(screen.getByLabelText(/married/i)).toBeInTheDocument();
  });

  it("renders number of children input", () => {
    renderForm();
    expect(screen.getByLabelText(/number of children/i)).toBeInTheDocument();
  });

  it("renders child age inputs for each child", () => {
    renderForm({ numChildren: 2, childAges: [5, 8] });
    expect(screen.getByLabelText(/age of child 1/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/age of child 2/i)).toBeInTheDocument();
  });

  it("renders earnings input", () => {
    renderForm();
    expect(
      screen.getByLabelText(/household wages and salaries/i),
    ).toBeInTheDocument();
  });

  it("renders calculate button", () => {
    renderForm();
    expect(
      screen.getByRole("button", { name: /calculate/i }),
    ).toBeInTheDocument();
  });

  it("calls onCalculate when button is clicked", async () => {
    const onCalculate = vi.fn();
    renderForm({ onCalculate });
    await userEvent.click(screen.getByRole("button", { name: /calculate/i }));
    expect(onCalculate).toHaveBeenCalledTimes(1);
  });

  it("shows loading text when loading", () => {
    renderForm({ loading: true });
    expect(screen.getByText(/calculating/i)).toBeInTheDocument();
  });
});
