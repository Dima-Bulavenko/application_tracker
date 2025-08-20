import RegisterForm from 'pages/auth/ui/RegisterForm';
import { AuthPage } from './AuthPage';

export function RegisterPage() {
  return (
    <AuthPage
      title='Create your account'
      subtitle='Start organizing your job applications today'
      footerText='Already have an account?'
      footerLinkText='Sign in'
      footerTo='/sign-in'>
      <RegisterForm />
    </AuthPage>
  );
}
