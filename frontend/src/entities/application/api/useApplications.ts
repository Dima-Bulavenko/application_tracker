import { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import { getApplications } from 'shared/api';
import { useSession } from 'shared/hooks';
import type {
  ApplicationOrderBy,
  ApplicationReadWithCompany,
} from 'shared/api/gen/types.gen';

export type UseApplicationsParams = {
  pageSize?: number;
  orderBy?: ApplicationOrderBy;
  orderDirection?: 'asc' | 'desc';
};

type State = {
  items: ApplicationReadWithCompany[];
  loading: boolean;
  error: string | null;
  hasMore: boolean;
};

export function useApplications(params?: UseApplicationsParams) {
  const { pageSize = 10, orderBy, orderDirection } = params ?? {};
  const { token } = useSession();
  const [state, setState] = useState<State>({
    items: [],
    loading: false,
    error: null,
    hasMore: true,
  });
  const offsetRef = useRef(0);
  const fetchingRef = useRef(false);

  const query = useMemo(
    () => ({
      limit: pageSize,
      order_by: orderBy,
      order_direction: orderDirection,
    }),
    [pageSize, orderBy, orderDirection]
  );

  const fetchPage = useCallback(async () => {
    if (fetchingRef.current || !state.hasMore) return;
    fetchingRef.current = true;
    setState((s) => ({ ...s, loading: true, error: null }));

    try {
      const res = await getApplications({
        query: { ...query, offset: offsetRef.current },
        throwOnError: true,
        headers: { Authorization: `Bearer ${token}` },
      });
      const data = res.data ?? [];
      setState((s) => ({
        items: [...s.items, ...data],
        loading: false,
        error: null,
        hasMore: data.length === (query.limit ?? 10),
      }));
      offsetRef.current += data.length;
    } catch (e: unknown) {
      const message =
        (e as { message?: string })?.message ?? 'Failed to load applications';
      setState((s) => ({ ...s, loading: false, error: message }));
    } finally {
      fetchingRef.current = false;
    }
  }, [query, state.hasMore]);

  const reset = useCallback(() => {
    offsetRef.current = 0;
    setState({ items: [], loading: false, error: null, hasMore: true });
  }, []);

  const refetch = useCallback(async () => {
    reset();
    await fetchPage();
  }, [reset, fetchPage]);

  useEffect(() => {
    // Reset and fetch when query params change
    reset();
  }, [query.limit, query.order_by, query.order_direction, reset]);

  useEffect(() => {
    // Initial fetch
    fetchPage();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return {
    items: state.items,
    loading: state.loading,
    error: state.error,
    hasMore: state.hasMore,
    loadMore: fetchPage,
    refetch,
  };
}
