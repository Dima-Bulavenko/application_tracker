import type { WorkLocation, WorkType } from 'shared/api/gen/types.gen';

export function humanizeWorkType(v?: WorkType) {
  if (!v) return undefined;
  return v
    .split('_')
    .map((s) => s.charAt(0).toUpperCase() + s.slice(1))
    .join(' ');
}

export function humanizeWorkLocation(v?: WorkLocation) {
  if (!v) return undefined;
  const map: Record<WorkLocation, string> = {
    on_site: 'On-site',
    remote: 'Remote',
    hybrid: 'Hybrid',
  };
  return map[v];
}
