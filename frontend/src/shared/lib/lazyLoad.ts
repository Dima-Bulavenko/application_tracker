import { lazy, ComponentType } from "react";

export function lazyImport<
  I,
  K extends keyof I,
>(
  factory: () => Promise<I>,
  name: K
): { [Key in K]: I[Key] } {
  return {
    [name]: lazy(() => factory().then(module => ({ default: module[name] as ComponentType }))) as unknown
  } as { [Key in K]: I[Key] };
}
