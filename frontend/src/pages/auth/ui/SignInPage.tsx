import SignInForm from 'pages/auth/ui/SignInForm';
import { AuthPage } from './AuthPage';

export function SignInPage() {
  return (
    <AuthPage
      title='Welcome back'
      subtitle='Sign in to continue tracking your applications'
      footerText="Don't have an account?"
      footerLinkText='Create one'
      footerTo='/register'>
      <SignInForm />
    </AuthPage>
  );
}
