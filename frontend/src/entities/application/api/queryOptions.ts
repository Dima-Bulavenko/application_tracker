import {
  createApplication,
  getApplicationById,
  getApplications,
  updateApplication,
  deleteApplication,
} from 'shared/api/gen/sdk.gen';
import type {
  ApplicationCreate,
  ApplicationUpdate,
  UpdateApplicationData,
  DeleteApplicationData,
  GetApplicationsData,
} from 'shared/api/gen/types.gen';
import { queryOptions, mutationOptions } from '@tanstack/react-query';

export const applicationKeys = {
  all: ['applications'],
  lists: () => [...applicationKeys.all, 'list'],
  list: (filters: GetApplicationsData['query']) => [
    ...applicationKeys.lists(),
    filters,
  ],
  details: () => [...applicationKeys.all, 'detail'],
  detail: (id: number) => [...applicationKeys.details(), id],
} as const;

export function applicationsOptions(filters?: GetApplicationsData['query']) {
  return queryOptions({
    queryKey: applicationKeys.list(filters),
    queryFn: () =>
      getApplications<true>({ query: filters }).then((res) => res.data ?? []),
    staleTime: Infinity,
  });
}

export function applicationOptions(application_id: number) {
  return queryOptions({
    queryKey: applicationKeys.detail(application_id),
    queryFn: async () =>
      getApplicationById<true>({ path: { application_id } }).then(
        (res) => res.data
      ),
    staleTime: Infinity,
  });
}

export function applicationCreateOptions() {
  return mutationOptions({
    mutationKey: applicationKeys.all,
    mutationFn: (body: ApplicationCreate) =>
      createApplication({ body }).then((r) => r.data),
  });
}

export function applicationUpdateOptions(
  application_id: UpdateApplicationData['path']['application_id']
) {
  return mutationOptions({
    mutationKey: applicationKeys.all,
    mutationFn: (body: ApplicationUpdate) =>
      updateApplication<true>({ body, path: { application_id } }).then(
        (res) => res.data
      ),
  });
}

export function applicationDeleteOptions(
  application_id: DeleteApplicationData['path']['application_id']
) {
  return mutationOptions({
    mutationKey: applicationKeys.all,
    mutationFn: async () =>
      deleteApplication<true>({ path: { application_id } }),
  });
}
