import type { QueryClient } from '@tanstack/react-query'
import { createRootRouteWithContext, Outlet } from '@tanstack/react-router'
import { TanStackRouterDevtools } from '@tanstack/react-router-devtools'
import { Suspense } from 'react'
import type { AccessTokenResponse, UserLogin } from 'shared/api/gen'
import type { AuthContextType } from 'shared/context/AuthContext'
import { SuspenseFallback } from 'shared/ui/SuspenseFallback'
import { Header } from 'widgets/header/ui/Header'

interface RouterContext {
  auth: AuthContextType & {
    logout: () => Promise<void>
    login: (data: UserLogin) => Promise<AccessTokenResponse>
    loginWithGoogle: (
      code: string,
      state: string
    ) => Promise<AccessTokenResponse>
    loginWithLinkedIn: (
      code: string,
      state: string
    ) => Promise<AccessTokenResponse>
  }
  queryClient: QueryClient
}

export const Route = createRootRouteWithContext<RouterContext>()({
  component: IndexComponent,
})

function IndexComponent() {
  return (
    <>
      <Header />
      <Suspense fallback={<SuspenseFallback />}>
        <Outlet />
      </Suspense>
      <TanStackRouterDevtools position='bottom-right' initialIsOpen={false} />
    </>
  )
}
