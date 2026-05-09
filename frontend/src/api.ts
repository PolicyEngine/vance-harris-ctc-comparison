// Next.js exposes browser-readable env vars as NEXT_PUBLIC_*; the default
// points at the Modal-hosted API used by the production deployment.
const API_URL =
  (typeof process !== "undefined" &&
    (process.env.NEXT_PUBLIC_API_URL || process.env.VITE_API_URL)) ||
  "https://policyengine--vance-harris-ctc-calculate.modal.run";

export interface CtcResults {
  baseline: number;
  harris: number;
  vance_non_refundable: number;
  vance_refundable: number;
  year: string;
}

export async function fetchCtcResults(
  isMarried: boolean,
  childAges: number[],
  earnings: number,
): Promise<CtcResults> {
  const params = new URLSearchParams({
    is_married: String(isMarried),
    num_children: String(childAges.length),
    child_ages: childAges.join(","),
    earnings: String(earnings),
  });

  const response = await fetch(`${API_URL}?${params}`);
  if (!response.ok) {
    throw new Error(`API error: ${response.status}`);
  }
  return response.json();
}
