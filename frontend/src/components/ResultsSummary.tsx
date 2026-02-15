import { Text, Title } from "@mantine/core";
import { colors } from "../designTokens";

interface ResultsSummaryProps {
  baseline: number;
  year: string;
}

export default function ResultsSummary({ baseline, year }: ResultsSummaryProps) {
  return (
    <Title order={2} ta="center" my="lg">
      In {year}, you will be eligible for a{" "}
      <Text component="span" c={colors.teal} fw={700} inherit>
        ${baseline.toLocaleString("en-US", { maximumFractionDigits: 0 })}
      </Text>{" "}
      child tax credit.
    </Title>
  );
}
