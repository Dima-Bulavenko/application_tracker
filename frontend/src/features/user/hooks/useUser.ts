import {
  getCurrentUser,
  googleCallback,
  linkedinCallback,
  login,
  logout,
  type UserLogin,
  type UserRead,
} from 'shared/api/gen'
import { client } from 'shared/api/gen/client.gen'
import { useAuth } from 'shared/hooks/useAuth'

type SetUser = (user: UserRead | null) => void

async function authenticateAndSetUser(
  accessToken: string,
  setUser: SetUser
): Promise<void> {
  client.setConfig({ auth: accessToken })
  try {
    const { data: user } = await getCurrentUser<true>()
    setUser(user)
  } catch (err) {
    client.setConfig({ auth: undefined })
    setUser(null)
    throw err
  }
}

export function useLogin() {
  const { setUser } = useAuth()

  return async (data: UserLogin) => {
    return login({ body: data }).then(async ({ data }) => {
      await authenticateAndSetUser(data.access_token, setUser)
      return data
    })
  }
}

export function useLogout() {
  const { setUser } = useAuth()
  return async () => {
    return logout<true>({}).then(() => {
      client.setConfig({ auth: undefined })
      setUser(null)
    })
  }
}

export function useLoginWithGoogle() {
  const { setUser } = useAuth()

  return async (code: string, state: string) => {
    return googleCallback({ query: { code, state } }).then(async ({ data }) => {
      await authenticateAndSetUser(data.access_token, setUser)
      return data
    })
  }
}

export function useLoginWithLinkedIn() {
  const { setUser } = useAuth()

  return async (code: string, state: string) => {
    return linkedinCallback({ query: { code, state } }).then(
      async ({ data }) => {
        await authenticateAndSetUser(data.access_token, setUser)
        return data
      }
    )
  }
}
