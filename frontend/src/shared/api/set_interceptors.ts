import { SessionContextType } from 'shared/context';
import { client } from './gen/client.gen';
import { refreshToken } from './gen';
const retryHeaderName = 'X-Retry';

export function setResponseInterceptor(
  setToken: NonNullable<SessionContextType['setToken']>
) {
  const interceptorId = client.instance.interceptors.response.use(
    (response) => {
      return response;
    },
    async (error) => {
      if (
        error?.status === 401 &&
        error?.config?.headers &&
        !error?.config?.headers[retryHeaderName]
      ) {
        error.config.headers[retryHeaderName] = true;
        const refreshResponse = await refreshToken({});
        if (refreshResponse.status === 200) {
          setToken(refreshResponse?.data?.access_token);
          error.config.headers['Authorization'] =
            `Bearer ${refreshResponse?.data?.access_token}`;
          return client.instance(error.config);
        }
      }
      return Promise.reject(error);
    }
  );

  return interceptorId;
}
