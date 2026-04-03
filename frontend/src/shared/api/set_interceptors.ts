import { client } from './gen/client.gen'
import { refreshToken } from './gen/sdk.gen'

const retryHeaderName = 'X-Retry'

let refreshPromise: Promise<string | undefined> | null = null

function refreshTokenOnce(): Promise<string | undefined> {
  if (!refreshPromise) {
    refreshPromise = refreshToken({})
      .then((res) => {
        if (res.status === 200) {
          const token = res.data?.access_token
          client.setConfig({ auth: token })
          return token
        }
        return undefined
      })
      .finally(() => {
        refreshPromise = null
      })
  }
  return refreshPromise
}

export function setResponseInterceptor() {
  const interceptorId = client.instance.interceptors.response.use(
    (response) => {
      return response
    },
    async (error) => {
      if (
        error?.status === 401 &&
        error?.config?.headers &&
        !error?.config?.headers[retryHeaderName]
      ) {
        error.config.headers[retryHeaderName] = true
        const newToken = await refreshTokenOnce()
        if (newToken) {
          error.config.headers['Authorization'] = `Bearer ${newToken}`
          return client.instance(error.config)
        }
      }
      return Promise.reject(error)
    }
  )

  return interceptorId
}
