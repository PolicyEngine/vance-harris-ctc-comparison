'use client';

import { useState } from "react";
import { Container, Title, MantineProvider, createTheme } from "@mantine/core";
import HouseholdForm from "./components/HouseholdForm";
import CtcChart from "./components/CtcChart";
import ResultsSummary from "./components/ResultsSummary";
import {
  BaselineDescription,
  ReformsDescription,
  Assumptions,
} from "./components/InfoSections";
import { fetchCtcResults, type CtcResults } from "./api";
import { fonts } from "./designTokens";

const theme = createTheme({
  fontFamily: fonts.body,
  primaryColor: "teal",
});

export default function App() {
  const [isMarried, setIsMarried] = useState(false);
  const [numChildren, setNumChildren] = useState(1);
  const [childAges, setChildAges] = useState<number[]>([5]);
  const [earnings, setEarnings] = useState(50000);
  const [results, setResults] = useState<CtcResults | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleCalculate = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await fetchCtcResults(isMarried, childAges, earnings);
      setResults(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Calculation failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <MantineProvider theme={theme}>
      <Container size="md" py="xl">
        <Title order={1} mb="md">
          Child tax credit calculator
        </Title>
        <BaselineDescription />
        <HouseholdForm
          isMarried={isMarried}
          setIsMarried={setIsMarried}
          numChildren={numChildren}
          setNumChildren={setNumChildren}
          childAges={childAges}
          setChildAges={setChildAges}
          earnings={earnings}
          setEarnings={setEarnings}
          onCalculate={handleCalculate}
          loading={loading}
        />
        {error && (
          <p style={{ color: "red" }} role="alert">
            {error}
          </p>
        )}
        {results && (
          <>
            <ResultsSummary baseline={results.baseline} year={results.year} />
            <ReformsDescription />
            <Title order={3} ta="center" mb="sm">
              Your 2025 child tax credit by policy
            </Title>
            <CtcChart results={results} />
          </>
        )}
        <Assumptions />
      </Container>
    </MantineProvider>
  );
}
