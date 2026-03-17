import { mutationOptions, queryOptions } from '@tanstack/react-query'
import {
  createApplication,
  deleteApplication,
  getApplicationById,
  getApplications,
  getUserCompanies,
  updateApplication,
} from 'shared/api/gen/sdk.gen'
import type {
  ApplicationCreate,
  ApplicationUpdate,
  DeleteApplicationData,
  GetApplicationsData,
  GetUserCompaniesData,
  UpdateApplicationData,
} from 'shared/api/gen/types.gen'

export const applicationKeys = {
  all: ['applications'],
  lists: () => [...applicationKeys.all, 'list'],
  list: (filters: GetApplicationsData['query']) => [
    ...applicationKeys.lists(),
    filters,
  ],
  details: () => [...applicationKeys.all, 'detail'],
  detail: (id: number) => [...applicationKeys.details(), id],
} as const

export function applicationsOptions(filters?: GetApplicationsData['query']) {
  return queryOptions({
    queryKey: applicationKeys.list(filters),
    queryFn: () =>
      getApplications({ query: filters }).then((res) => res.data ?? []),
    staleTime: Infinity,
  })
}

export function applicationOptions(application_id: number) {
  return queryOptions({
    queryKey: applicationKeys.detail(application_id),
    queryFn: async () =>
      getApplicationById({ path: { application_id } }).then((res) => res.data),
    staleTime: Infinity,
  })
}

export function applicationCreateOptions() {
  return mutationOptions({
    mutationKey: applicationKeys.all,
    mutationFn: (body: ApplicationCreate) =>
      createApplication({ body }).then((r) => r.data),
  })
}

export function applicationUpdateOptions(
  application_id: UpdateApplicationData['path']['application_id']
) {
  return mutationOptions({
    mutationKey: applicationKeys.all,
    mutationFn: (body: ApplicationUpdate) =>
      updateApplication({ body, path: { application_id } }).then(
        (res) => res.data
      ),
  })
}

export function applicationDeleteOptions(
  application_id: DeleteApplicationData['path']['application_id']
) {
  return mutationOptions({
    mutationKey: applicationKeys.all,
    mutationFn: async () => deleteApplication({ path: { application_id } }),
  })
}

export const companyKeys = {
  all: ['companies'],
  lists: () => [...companyKeys.all, 'list'],
  list: (filters: GetUserCompaniesData['query']) => [
    ...companyKeys.lists(),
    filters,
  ],
  details: () => [...companyKeys.all, 'detail'],
  detail: (id: number) => [...companyKeys.details(), id],
} as const

export function userCompaniesOptions(filters?: GetUserCompaniesData['query']) {
  return queryOptions({
    queryKey: companyKeys.list(filters),
    queryFn: () =>
      getUserCompanies({ query: filters }).then((res) => res.data ?? []),
    staleTime: Infinity,
  })
}
