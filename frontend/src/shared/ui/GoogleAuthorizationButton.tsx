import { googleAuthorize } from 'shared/api/gen';
import SocialAuthorizationButton from './SocialAuthorizationButton';

interface GoogleAuthorizationButtonProps {
  action?: 'sign-in' | 'sign-up';
  disabled?: boolean;
}

export default function GoogleAuthorizationButton({
  action = 'sign-in',
  disabled = false,
}: GoogleAuthorizationButtonProps) {
  const buttonText =
    action === 'sign-up' ? 'Sign up with Google' : 'Sign in with Google';

  return (
    <SocialAuthorizationButton
      provider='Google'
      onAuthorize={googleAuthorize}
      buttonText={buttonText}
      disabled={disabled}
    />
  );
}
