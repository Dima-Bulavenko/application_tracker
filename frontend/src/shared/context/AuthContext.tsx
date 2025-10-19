import React from 'react';
import type { UserRead } from 'shared/api/gen';

export type AuthContextType = (
  | { user: UserRead; isAuthenticated: true }
  | { user: null; isAuthenticated: false }
) & { setUser: React.Dispatch<React.SetStateAction<UserRead | null>> };

export const AuthContext = React.createContext<AuthContextType | null>(null);
