import { createFileRoute, SearchSchemaInput } from '@tanstack/react-router';
import { applicationsOptions } from 'entities/application/api/queryOptions';
import { DashboardPage } from 'pages/dashboard/ui/DashboardPage';
import { zGetApplicationsData } from 'shared/api/gen/zod.gen';
import z from 'zod';

const ApplicationFilterSchema = zGetApplicationsData.shape.query;

type ApplicationFilterSchemaType = z.infer<typeof ApplicationFilterSchema>;

const defaultFilterParams = {
  limit: 10,
  offset: 0,
  order_by: 'time_create',
  order_direction: 'desc',
  status: [],
  work_type: [],
  work_location: [],
  company_name: 'gav',
};

const filterParams = JSON.parse(
  localStorage.getItem('appFilters') || JSON.stringify(defaultFilterParams)
);

export const Route = createFileRoute('/_authenticated/dashboard')({
  validateSearch: (
    search: {
      filter?: Partial<ApplicationFilterSchemaType>;
    } & SearchSchemaInput
  ) => ({
    filter: ApplicationFilterSchema.parse(search.filter || filterParams),
  }),
  loaderDeps: ({ search: { filter } }) => ({ filter }),
  loader: ({ context: { queryClient }, deps: { filter } }) =>
    queryClient.ensureQueryData(applicationsOptions(filter)),
  component: RouteComponent,
});

function RouteComponent() {
  return <DashboardPage />;
}
