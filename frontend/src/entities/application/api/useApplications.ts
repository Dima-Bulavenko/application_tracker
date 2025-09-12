import {
  createApplication,
  getApplicationById,
  getApplications,
  updateApplication,
} from 'shared/api';
import type {
  ApplicationCreate,
  ApplicationUpdate,
  UpdateApplicationData,
} from 'shared/api';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { GetApplicationsData } from 'shared/api';

export function useApplicationsList(params?: GetApplicationsData['query']) {
  return useQuery({
    queryKey: ['applications', params],
    queryFn: async () => {
      const res = await getApplications({ query: { ...params } });
      return res.data ?? [];
    },
    staleTime: 30_000,
  });
}

export function useCreateApplication() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (body: ApplicationCreate) =>
      createApplication({ body }).then((r) => r.data),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ['applications'] });
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
      qc.invalidateQueries({ queryKey: ['applications'] });
    },
  });
}

export function useGetApplication(
  application_id: UpdateApplicationData['path']['application_id']
) {
  return useQuery({
    queryKey: ['applications', application_id],
    queryFn: () =>
      getApplicationById<true>({ path: { application_id } }).then(
        (response) => response.data
      ),
    staleTime: 30_000,
  });
}
