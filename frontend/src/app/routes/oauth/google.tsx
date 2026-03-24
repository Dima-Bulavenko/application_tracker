import { createFileRoute, Navigate } from '@tanstack/react-router'
import { AxiosError } from 'axios'
import { zGoogleCallbackData } from 'shared/api/gen/zod.gen'
import GoogleAuthorizationButton from 'shared/ui/GoogleAuthorizationButton'
import OAuthError from 'shared/ui/OAuthError'

const zSearchPramsSchema = zGoogleCallbackData.shape.query

export const Route = createFileRoute('/oauth/google')({
  validateSearch: zSearchPramsSchema,
  loaderDeps: ({ search }) => search,
  loader: async ({ deps, context }) => {
    const { code, state } = deps
    const { loginWithGoogle } = context.auth
    const res = await loginWithGoogle(code, state)
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
        authButton={<GoogleAuthorizationButton action='sign-in' />}
        errorMessage={message}
        provider={provider}
      />
    )
  }

  return (
    <OAuthError authButton={<GoogleAuthorizationButton action='sign-in' />} />
  )
}
