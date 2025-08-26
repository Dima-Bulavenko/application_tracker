/**
 * Format an ISO date string into a localized date string.
 * Returns undefined for falsy input and passes through invalid dates.
 */
export function formatDate(value?: string | null): string | undefined {
  if (!value) return undefined;
  const d = new Date(value);
  return Number.isNaN(d.getTime()) ? value : d.toLocaleDateString();
}
