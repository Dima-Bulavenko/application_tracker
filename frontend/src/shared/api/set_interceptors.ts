import { client } from './gen/client.gen';
import { refreshToken } from './gen/sdk.gen';
const retryHeaderName = 'X-Retry';

export function setResponseInterceptor() {
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
          client.setConfig({ auth: refreshResponse.data?.access_token });
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
