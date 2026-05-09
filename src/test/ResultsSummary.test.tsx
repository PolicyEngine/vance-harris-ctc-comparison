import { describe, it, expect } from "vitest";
import { render, screen } from "@testing-library/react";
import { MantineProvider } from "@mantine/core";
import ResultsSummary from "../components/ResultsSummary";

describe("ResultsSummary", () => {
  it("displays the baseline CTC amount", () => {
    render(
      <MantineProvider>
        <ResultsSummary baseline={2000} year="2025" />
      </MantineProvider>,
    );
    expect(screen.getByText(/\$2,000/)).toBeInTheDocument();
  });

  it("displays the year", () => {
    render(
      <MantineProvider>
        <ResultsSummary baseline={2000} year="2025" />
      </MantineProvider>,
    );
    expect(screen.getByText(/2025/)).toBeInTheDocument();
  });
});
