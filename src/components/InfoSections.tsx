import { Text, Anchor, List, Stack } from "@mantine/core";

export function BaselineDescription() {
  return (
    <Stack gap="xs" mb="md">
      <Text>
        The current child tax credit provides up to $2,000 per qualifying child,
        phasing in and out with income. Enter your expected 2025 information
        below to see how much you'll be eligible for.
      </Text>
      <Anchor
        href="https://policyengine.org/us/research/the-child-tax-credit-in-2023"
        target="_blank"
        rel="noopener"
        size="sm"
      >
        Learn more about the current child tax credit
      </Anchor>
    </Stack>
  );
}

export function ReformsDescription() {
  return (
    <Stack gap="xs" my="md">
      <Text>
        Members of the Democratic and Republican presidential tickets have
        indicated interest in expanding the child tax credit:
      </Text>
      <List size="sm" spacing="xs">
        <List.Item>
          <Text size="sm">
            <b>Harris-Walz CTC plan</b>: Restores the 2021 expansion making it
            fully refundable and more generous, adding a $2,400 "baby bonus".{" "}
            <Anchor
              href="https://policyengine.org/us/research/harris-ctc"
              target="_blank"
              rel="noopener"
              size="sm"
            >
              Read our full report.
            </Anchor>
          </Text>
        </List.Item>
        <List.Item>
          <Text size="sm">
            <b>Vance CTC suggestion</b>: Senator Vance suggested expanding the
            CTC to $5,000. We modeled both refundable and non-refundable
            scenarios.{" "}
            <Anchor
              href="https://policyengine.org/us/research/vance-ctc"
              target="_blank"
              rel="noopener"
              size="sm"
            >
              Read our full report.
            </Anchor>
          </Text>
        </List.Item>
      </List>
      <Text size="sm">
        The chart below shows how these reforms would affect your child tax
        credit:
      </Text>
    </Stack>
  );
}

export function Assumptions() {
  return (
    <Stack gap="xs" mt="xl">
      <Text fw={600} size="sm">
        Assumptions
      </Text>
      <List size="xs" spacing={4}>
        <List.Item>
          All earnings are from the tax filer's wages, salaries, and tips in
          2025.
        </List.Item>
        <List.Item>The filer has no other taxable income.</List.Item>
        <List.Item>The filer takes the standard deduction.</List.Item>
        <List.Item>Married couples file jointly.</List.Item>
        <List.Item>
          Senator JD Vance's suggestion has the same age limit as the current
          CTC.
        </List.Item>
        <List.Item>Uses the policyengine-us Python package.</List.Item>
      </List>
    </Stack>
  );
}
