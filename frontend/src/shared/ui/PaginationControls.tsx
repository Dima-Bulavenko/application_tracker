import {
  Pagination,
  PaginationContent,
  PaginationEllipsis,
  PaginationItem,
  PaginationLink,
  PaginationNext,
  PaginationPrevious,
} from 'app/components/ui/pagination'

interface PaginationControlsProps {
  currentPage: number
  totalPages: number
  onPageChange: (page: number) => void
}

const MAX_VISIBLE_PAGES = 7

function getPageItems(
  currentPage: number,
  totalPages: number
): Array<number | 'ellipsis'> {
  if (totalPages <= MAX_VISIBLE_PAGES) {
    return Array.from({ length: totalPages }, (_, idx) => idx + 1)
  }

  const pageItems: Array<number | 'ellipsis'> = [1]

  let start = Math.max(2, currentPage - 1)
  let end = Math.min(totalPages - 1, currentPage + 1)

  if (currentPage <= 3) {
    start = 2
    end = 4
  }

  if (currentPage >= totalPages - 2) {
    start = totalPages - 3
    end = totalPages - 1
  }

  if (start > 2) {
    pageItems.push('ellipsis')
  }

  for (let page = start; page <= end; page += 1) {
    pageItems.push(page)
  }

  if (end < totalPages - 1) {
    pageItems.push('ellipsis')
  }

  pageItems.push(totalPages)

  return pageItems
}

export function PaginationControls({
  currentPage,
  totalPages,
  onPageChange,
}: PaginationControlsProps) {
  if (totalPages <= 1) {
    return null
  }

  const pageItems = getPageItems(currentPage, totalPages)

  const handlePageChange = (page: number) => {
    if (page >= 1 && page <= totalPages && page !== currentPage) {
      onPageChange(page)
    }
  }

  return (
    <Pagination>
      <PaginationContent>
        <PaginationItem>
          <PaginationPrevious
            href='#'
            aria-disabled={currentPage <= 1}
            className={
              currentPage <= 1 ? 'pointer-events-none opacity-50' : undefined
            }
            onClick={(event) => {
              event.preventDefault()
              handlePageChange(currentPage - 1)
            }}
          />
        </PaginationItem>

        {pageItems.map((pageItem, idx) => {
          if (pageItem === 'ellipsis') {
            return (
              <PaginationItem key={`ellipsis-${idx}`}>
                <PaginationEllipsis />
              </PaginationItem>
            )
          }

          return (
            <PaginationItem key={pageItem}>
              <PaginationLink
                href='#'
                isActive={pageItem === currentPage}
                onClick={(event) => {
                  event.preventDefault()
                  handlePageChange(pageItem)
                }}
              >
                {pageItem}
              </PaginationLink>
            </PaginationItem>
          )
        })}

        <PaginationItem>
          <PaginationNext
            href='#'
            aria-disabled={currentPage >= totalPages}
            className={
              currentPage >= totalPages
                ? 'pointer-events-none opacity-50'
                : undefined
            }
            onClick={(event) => {
              event.preventDefault()
              handlePageChange(currentPage + 1)
            }}
          />
        </PaginationItem>
      </PaginationContent>
    </Pagination>
  )
}
