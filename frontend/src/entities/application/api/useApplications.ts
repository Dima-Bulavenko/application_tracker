import {
  createApplication,
  getApplicationById,
  getApplications,
  updateApplication,
  deleteApplication,
} from 'shared/api';
import type {
  ApplicationCreate,
  ApplicationUpdate,
  UpdateApplicationData,
  DeleteApplicationData,
  ApplicationReadWithCompany,
} from 'shared/api';
import {
  useQuery,
  useMutation,
  useQueryClient,
  type UseQueryOptions,
} from '@tanstack/react-query';
import { type GetApplicationsData } from 'shared/api';

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

export function useApplicationsList(
  filters?: GetApplicationsData['query'],
  options?: Omit<
    UseQueryOptions<
      ApplicationReadWithCompany[],
      Error,
      ApplicationReadWithCompany[],
      ReturnType<typeof applicationKeys.list>
    >,
    'queryKey' | 'queryFn'
  >
) {
  return useQuery({
    ...options,
    queryKey: applicationKeys.list(filters),
    queryFn: async () => {
      const res = await getApplications<true>({ query: { ...filters } });
      return res.data ?? [];
    },
  });
}

export function useCreateApplication() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (body: ApplicationCreate) =>
      createApplication({ body }).then((r) => r.data),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: applicationKeys.all });
    },
  });
}

export function useUpdateApplication(
  application_id: UpdateApplicationData['path']['application_id']
) {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (body: ApplicationUpdate) =>
      updateApplication<true>({ body, path: { application_id } }).then(
        (response) => response.data
      ),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: applicationKeys.all });
    },
  });
}

export function useGetApplication(
  application_id: UpdateApplicationData['path']['application_id']
) {
  return useQuery({
    queryKey: applicationKeys.detail(application_id),
    queryFn: () =>
      getApplicationById<true>({ path: { application_id } }).then(
        (response) => response.data
      ),
    staleTime: 30_000,
  });
}

export function useDeleteApplication(
  application_id: DeleteApplicationData['path']['application_id']
) {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: async () => {
      const response = await deleteApplication<true>({
        path: { application_id },
      });
      return response.data;
    },
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: applicationKeys.all });
    },
  });
}
