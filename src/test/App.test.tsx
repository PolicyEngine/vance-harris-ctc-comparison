import { describe, it, expect } from "vitest";
import { render, screen } from "@testing-library/react";
import App from "../App";

describe("App", () => {
  it("renders the title", () => {
    render(<App />);
    expect(
      screen.getByRole("heading", { name: /child tax credit calculator/i }),
    ).toBeInTheDocument();
  });

  it("renders the form", () => {
    render(<App />);
    expect(
      screen.getByRole("button", { name: /calculate/i }),
    ).toBeInTheDocument();
  });

  it("renders assumptions section", () => {
    render(<App />);
    expect(screen.getByText(/assumptions/i)).toBeInTheDocument();
  });

  it("does not show results before calculation", () => {
    render(<App />);
    expect(screen.queryByTestId("ctc-chart")).not.toBeInTheDocument();
  });
});
