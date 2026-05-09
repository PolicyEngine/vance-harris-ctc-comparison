import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  Cell,
  LabelList,
  ResponsiveContainer,
} from "recharts";
import { colors } from "../designTokens";
import type { CtcResults } from "../api";

interface CtcChartProps {
  results: CtcResults;
}

interface ChartDatum {
  name: string;
  value: number;
  color: string;
  diff: number;
}

const formatDollars = (v: number) =>
  `$${v.toLocaleString("en-US", { maximumFractionDigits: 0 })}`;

function buildChartData(results: CtcResults): ChartDatum[] {
  const items: ChartDatum[] = [
    {
      name: "Vance suggestion (refundable possibility)",
      value: results.vance_refundable,
      color: colors.lightRed,
      diff: results.vance_refundable - results.baseline,
    },
    {
      name: "Vance suggestion (non-refundable possibility)",
      value: results.vance_non_refundable,
      color: colors.lighterRed,
      diff: results.vance_non_refundable - results.baseline,
    },
    {
      name: "Harris-Walz plan",
      value: results.harris,
      color: colors.blue,
      diff: results.harris - results.baseline,
    },
    {
      name: "Baseline",
      value: results.baseline,
      color: colors.gray,
      diff: 0,
    },
  ];
  // Sort: Baseline last, others by value descending
  return items.sort((a, b) => {
    if (a.name === "Baseline") return 1;
    if (b.name === "Baseline") return -1;
    return b.value - a.value;
  });
}

function DiffLabel(props: {
  x?: number;
  y?: number;
  width?: number;
  height?: number;
  value?: number;
  index?: number;
  data: ChartDatum[];
}) {
  const { x = 0, width = 0, y = 0, height = 0, index = 0, data } = props;
  const item = data[index];
  if (!item || item.name === "Baseline") return null;
  const diff = item.diff;
  const label = diff >= 0 ? `+${formatDollars(diff)}` : `-${formatDollars(-diff)}`;
  return (
    <text
      x={x + width + 8}
      y={y + height / 2}
      textAnchor="start"
      dominantBaseline="middle"
      fontSize={14}
      fill={colors.darkGray}
    >
      {label}
    </text>
  );
}

export default function CtcChart({ results }: CtcChartProps) {
  const data = buildChartData(results);

  return (
    <div data-testid="ctc-chart">
      <ResponsiveContainer width="100%" height={300}>
        <BarChart
          data={data}
          layout="vertical"
          margin={{ top: 10, right: 120, left: 20, bottom: 10 }}
        >
          <XAxis
            type="number"
            tickFormatter={formatDollars}
            tick={{ fontSize: 13 }}
          />
          <YAxis
            type="category"
            dataKey="name"
            width={260}
            tick={{ fontSize: 13 }}
          />
          <Tooltip
            formatter={(value) => formatDollars(Number(value))}
            labelStyle={{ fontWeight: 600 }}
          />
          <Bar dataKey="value" barSize={36}>
            {data.map((entry, index) => (
              <Cell key={index} fill={entry.color} />
            ))}
            <LabelList
              dataKey="value"
              position="inside"
              formatter={(v) => formatDollars(Number(v))}
              style={{ fill: colors.white, fontWeight: 700, fontSize: 15 }}
            />
            <LabelList
              dataKey="value"
              content={<DiffLabel data={data} />}
            />
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}

export { buildChartData, formatDollars };
