import { type GetApplicationsData } from 'shared/api';
import { type useApplicationsList } from './useApplications';

export type FilterForm = Omit<
  NonNullable<GetApplicationsData['query']>,
  'limit' | 'offset'
>;

export type AppListQueryRes = ReturnType<typeof useApplicationsList>;
