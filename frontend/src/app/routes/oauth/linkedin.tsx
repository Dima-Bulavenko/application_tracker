import { createFileRoute, Navigate } from '@tanstack/react-router'
import { AxiosError } from 'axios'
import { zLinkedinCallbackData } from 'shared/api/gen/zod.gen'
import LinkedInAuthorizationButton from 'shared/ui/LinkedInAuthorizationButton'
import OAuthError from 'shared/ui/OAuthError'

const zSearchPramsSchema = zLinkedinCallbackData.shape.query

export const Route = createFileRoute('/oauth/linkedin')({
  validateSearch: zSearchPramsSchema,
  loaderDeps: ({ search }) => search,
  loader: async ({ deps, context }) => {
    const { code, state } = deps
    const { loginWithLinkedIn } = context.auth
    const res = await loginWithLinkedIn(code, state)
    return res
  },
  component: RouteComponent,
  errorComponent: ErrorRouteComponent,
})

function RouteComponent() {
  return <Navigate to={'/dashboard'} replace={true} />
}

function ErrorRouteComponent({ error }: { error: Error }) {
  if (
    error instanceof AxiosError &&
    error.response?.data?.detail?.error_code === 'ACCOUNT_LINKED_TO_PROVIDER'
  ) {
    const { message, provider } = error.response.data.detail
    return (
      <OAuthError
        authButton={<LinkedInAuthorizationButton action='sign-in' />}
        errorMessage={message}
        provider={provider}
      />
    )
  }

  return (
    <OAuthError authButton={<LinkedInAuthorizationButton action='sign-in' />} />
  )
}
