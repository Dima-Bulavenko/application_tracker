import { useEffect, useMemo, useReducer, useCallback } from 'react';
import {
  refreshToken,
  getCurrentUser,
  type UserRead,
  client,
  setResponseInterceptor,
} from 'shared/api';
import { SessionContext } from 'shared/context/SessionContext';

interface SessionState {
  token?: string;
  user?: UserRead;
  isFetching: boolean;
}

type SessionAction =
  | { type: 'SET_FETCHING'; payload: boolean }
  | { type: 'SET_TOKEN'; payload: string | undefined }
  | { type: 'SET_USER'; payload: UserRead | undefined }
  | { type: 'RESET_SESSION' };

function sessionReducer(
  state: SessionState,
  action: SessionAction
): SessionState {
  switch (action.type) {
    case 'SET_FETCHING':
      return { ...state, isFetching: action.payload };
    case 'SET_TOKEN':
      return { ...state, token: action.payload };
    case 'SET_USER':
      return { ...state, user: action.payload, isFetching: false };
    case 'RESET_SESSION':
      return { token: undefined, user: undefined, isFetching: false };
    default:
      return state;
  }
}

const initialState: SessionState = {
  token: undefined,
  user: undefined,
  isFetching: false,
};

export function SessionProvider({ children }: React.PropsWithChildren<object>) {
  const [state, dispatch] = useReducer(sessionReducer, initialState);
  const { token, user, isFetching } = state;

  const setToken = useCallback((token: string | undefined) => {
    dispatch({ type: 'SET_TOKEN', payload: token });
  }, []);

  const setUser = useCallback((user: UserRead | undefined) => {
    dispatch({ type: 'SET_USER', payload: user });
  }, []);

  useEffect(() => {
    dispatch({ type: 'SET_FETCHING', payload: true });
    refreshToken<true>({})
      .then(async ({ data: { access_token } }) => {
        setToken(access_token);
        client.setConfig({ auth: access_token });
        const { data: user } = await getCurrentUser<true>();
        setUser(user);
      })
      .catch(() => dispatch({ type: 'RESET_SESSION' }))
      .finally(() => dispatch({ type: 'SET_FETCHING', payload: false }));
  }, [setToken, setUser]);

  useEffect(() => {
    client.setConfig({ auth: token });
  }, [token]);

  useEffect(() => {
    if (!token) return;
    const responseIntId = setResponseInterceptor(setToken);
    return () => {
      client.instance.interceptors.response.eject(responseIntId);
    };
  }, [setToken, token]);

  const value = useMemo(
    () => ({
      user,
      token,
      isFetching,
      setToken,
      setUser,
    }),
    [user, token, isFetching, setToken, setUser]
  );

  return (
    <SessionContext.Provider value={value}>{children}</SessionContext.Provider>
  );
}
