import type { QueryClient } from '@tanstack/react-query'
import {
  createRootRouteWithContext,
  HeadContent,
  Outlet,
} from '@tanstack/react-router'
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
  head: () => ({
    meta: [{ title: 'Application Tracker' }],
  }),
  component: IndexComponent,
})

function IndexComponent() {
  return (
    <>
      <HeadContent />
      <Header />
      <Suspense fallback={<SuspenseFallback />}>
        <Outlet />
      </Suspense>
      <TanStackRouterDevtools position='bottom-right' initialIsOpen={false} />
    </>
  )
}
