import { linkedinAuthorize } from 'shared/api/gen';
import SocialAuthorizationButton from './SocialAuthorizationButton';

interface LinkedInAuthorizationButtonProps {
  action?: 'sign-in' | 'sign-up';
  disabled?: boolean;
}

export default function LinkedInAuthorizationButton({
  action = 'sign-in',
  disabled = false,
}: LinkedInAuthorizationButtonProps) {
  const buttonText =
    action === 'sign-up' ? 'Sign up with LinkedIn' : 'Sign in with LinkedIn';

  return (
    <SocialAuthorizationButton
      provider='LinkedIn'
      onAuthorize={linkedinAuthorize}
      buttonText={buttonText}
      disabled={disabled}
    />
  );
}
