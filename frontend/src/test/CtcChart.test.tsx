import { describe, it, expect } from "vitest";
import { render, screen } from "@testing-library/react";
import CtcChart, { buildChartData, formatDollars } from "../components/CtcChart";
import type { CtcResults } from "../api";

const sampleResults: CtcResults = {
  baseline: 2000,
  harris: 3600,
  vance_non_refundable: 2967,
  vance_refundable: 5000,
  year: "2025",
};

describe("formatDollars", () => {
  it("formats numbers as dollar amounts", () => {
    expect(formatDollars(2000)).toBe("$2,000");
    expect(formatDollars(3600)).toBe("$3,600");
    expect(formatDollars(0)).toBe("$0");
  });
});

describe("buildChartData", () => {
  it("returns four items with correct names", () => {
    const data = buildChartData(sampleResults);
    expect(data).toHaveLength(4);
    const names = data.map((d) => d.name);
    expect(names).toContain("Baseline");
    expect(names).toContain("Harris-Walz plan");
    expect(names).toContain("Vance suggestion (refundable possibility)");
    expect(names).toContain("Vance suggestion (non-refundable possibility)");
  });

  it("puts Baseline last", () => {
    const data = buildChartData(sampleResults);
    expect(data[data.length - 1].name).toBe("Baseline");
  });

  it("calculates diff from baseline", () => {
    const data = buildChartData(sampleResults);
    const harris = data.find((d) => d.name === "Harris-Walz plan")!;
    expect(harris.diff).toBe(1600);
    const baseline = data.find((d) => d.name === "Baseline")!;
    expect(baseline.diff).toBe(0);
  });
});

describe("CtcChart", () => {
  it("renders without crashing", () => {
    render(<CtcChart results={sampleResults} />);
    expect(screen.getByTestId("ctc-chart")).toBeInTheDocument();
  });
});
