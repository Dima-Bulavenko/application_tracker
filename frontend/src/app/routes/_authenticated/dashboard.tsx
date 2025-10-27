import { createFileRoute, SearchSchemaInput } from '@tanstack/react-router';
import { applicationsOptions } from 'entities/application/api/queryOptions';
import { DashboardPage } from 'pages/dashboard/ui/DashboardPage';
import {
  ApplicationFilter,
  filterStorage,
  hasFilters,
  parseFilters,
} from 'features/application/lib/filterStorage';

type SearchParams = { filter?: ApplicationFilter } & SearchSchemaInput;

const resolveFilters = (
  search: SearchParams
): ApplicationFilter | undefined => {
  // Priority 1: Explicit URL params (with validation)
  if (hasFilters(search.filter)) {
    const parsed = parseFilters(search.filter);
    if (parsed && hasFilters(parsed)) {
      return parsed;
    }
  }

  // Priority 2: Stored filters from previous session
  const storedFilters = filterStorage.get();
  if (storedFilters) {
    const parsed = parseFilters(storedFilters);
    if (parsed && hasFilters(parsed)) {
      return parsed;
    }
  }

  return undefined;
};

export const Route = createFileRoute('/_authenticated/dashboard')({
  validateSearch: (search: SearchParams) => {
    const filter = resolveFilters(search);
    return filter ? { filter } : {};
  },
  loaderDeps: ({ search: { filter } }) => ({ filter }),
  loader: ({ context: { queryClient }, deps: { filter } }) =>
    queryClient.ensureQueryData(applicationsOptions(filter)),
  component: DashboardPage,
});
