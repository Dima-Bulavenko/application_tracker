export function getPaginationPrams(page: number, pageSize: number = 10) {
  return {
    limit: pageSize,
    offset: (page - 1) * pageSize,
  }
}
