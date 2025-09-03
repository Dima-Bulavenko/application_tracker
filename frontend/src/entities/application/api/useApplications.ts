import { createApplication, getApplications } from 'shared/api';
import type { ApplicationCreate } from 'shared/api';
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
