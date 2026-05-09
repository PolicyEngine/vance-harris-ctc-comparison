import {
  Checkbox,
  NumberInput,
  Button,
  Stack,
  Group,
  Text,
} from "@mantine/core";

interface HouseholdFormProps {
  isMarried: boolean;
  setIsMarried: (v: boolean) => void;
  numChildren: number;
  setNumChildren: (v: number) => void;
  childAges: number[];
  setChildAges: (v: number[]) => void;
  earnings: number;
  setEarnings: (v: number) => void;
  onCalculate: () => void;
  loading: boolean;
}

export default function HouseholdForm({
  isMarried,
  setIsMarried,
  numChildren,
  setNumChildren,
  childAges,
  setChildAges,
  earnings,
  setEarnings,
  onCalculate,
  loading,
}: HouseholdFormProps) {
  const handleNumChildrenChange = (val: string | number) => {
    const n = typeof val === "string" ? parseInt(val, 10) || 0 : val;
    const clamped = Math.max(0, Math.min(10, n));
    setNumChildren(clamped);
    const newAges = [...childAges];
    while (newAges.length < clamped) newAges.push(5);
    setChildAges(newAges.slice(0, clamped));
  };

  const handleChildAgeChange = (index: number, val: string | number) => {
    const age = typeof val === "string" ? parseInt(val, 10) || 0 : val;
    const newAges = [...childAges];
    newAges[index] = Math.max(0, Math.min(16, age));
    setChildAges(newAges);
  };

  return (
    <Stack gap="md">
      <Checkbox
        label="I'm married"
        checked={isMarried}
        onChange={(e) => setIsMarried(e.currentTarget.checked)}
      />
      <NumberInput
        label="Number of children"
        value={numChildren}
        onChange={handleNumChildrenChange}
        min={0}
        max={10}
      />
      {childAges.map((age, i) => (
        <NumberInput
          key={i}
          label={`Age of child ${i + 1}`}
          value={age}
          onChange={(val) => handleChildAgeChange(i, val)}
          min={0}
          max={16}
        />
      ))}
      <NumberInput
        label="Household wages and salaries in 2025"
        value={earnings}
        onChange={(val) =>
          setEarnings(typeof val === "string" ? parseInt(val, 10) || 0 : val)
        }
        min={0}
        max={300000}
        step={1000}
        thousandSeparator=","
        prefix="$"
      />
      <Group>
        <Button
          onClick={onCalculate}
          loading={loading}
          color="#319795"
          size="md"
        >
          Calculate my CTC
        </Button>
      </Group>
      {loading && (
        <Text size="sm" c="dimmed">
          Calculating... this may take up to 30 seconds on first load.
        </Text>
      )}
    </Stack>
  );
}
