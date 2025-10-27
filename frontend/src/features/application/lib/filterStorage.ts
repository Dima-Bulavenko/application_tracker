import { zGetApplicationsData } from 'shared/api/gen/zod.gen';
import z from 'zod';

const querySchema = zGetApplicationsData.shape.query.unwrap().shape;

// Schema with .catch() to handle invalid values gracefully
export const ApplicationFilterSchema = z.object({
  order_by: querySchema.order_by.catch(undefined),
  order_direction: querySchema.order_direction.catch(undefined),
  status: querySchema.status.catch(undefined),
  work_type: querySchema.work_type.catch(undefined),
  work_location: querySchema.work_location.catch(undefined),
  company_name: querySchema.company_name.catch(undefined),
});

export type ApplicationFilter = z.infer<typeof ApplicationFilterSchema>;

const FILTER_STORAGE_KEY = 'appFilters' as const;

const isEmptyValue = (value: unknown): boolean => {
  if (value === undefined || value === null) return true;
  if (Array.isArray(value) && value.length === 0) return true;
  return false;
};

export const hasFilters = (
  filter?: ApplicationFilter
): filter is ApplicationFilter => {
  return Boolean(filter && Object.keys(filter).length > 0);
};

export const parseFilters = (data: unknown): ApplicationFilter | null => {
  try {
    return ApplicationFilterSchema.parse(data);
  } catch {
    // Invalid filter data - return null to ignore it
    return null;
  }
};

export const cleanFilterData = (
  data: ApplicationFilter
): Partial<ApplicationFilter> => {
  return Object.fromEntries(
    Object.entries(data).filter(([, value]) => !isEmptyValue(value))
  );
};

export const filterStorage = {
  save: (filters: Partial<ApplicationFilter>): void => {
    localStorage.setItem(FILTER_STORAGE_KEY, JSON.stringify(filters));
  },

  clear: (): void => {
    localStorage.removeItem(FILTER_STORAGE_KEY);
  },

  get: (): ApplicationFilter | null => {
    try {
      const stored = localStorage.getItem(FILTER_STORAGE_KEY);
      if (!stored) return null;

      const parsed = JSON.parse(stored);
      // Validate and clean invalid values
      const validated = ApplicationFilterSchema.parse(parsed);
      return validated;
    } catch {
      // Clear corrupted data
      localStorage.removeItem(FILTER_STORAGE_KEY);
      return null;
    }
  },
};
