import Button from '@mui/material/Button';
import { ReactNode, useState } from 'react';

interface SocialSignInButtonProps {
  provider: string;
  icon?: ReactNode;
  onAuthorize: () => Promise<{
    status: number;
    data: { authorization_url: string };
  }>;
  disabled?: boolean;
  buttonText?: string;
}

export default function SocialAuthorizationButton({
  provider,
  icon,
  onAuthorize,
  buttonText,
  disabled = false,
}: SocialSignInButtonProps) {
  const [isLoading, setIsLoading] = useState(false);
  const handleClick = async () => {
    setIsLoading(true);
    try {
      const res = await onAuthorize();
      if (res.status === 200) {
        window.location.href = res.data.authorization_url;
      }
    } catch (error) {
      console.error(`${provider} authorization failed:`, error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Button
      type='button'
      variant='outlined'
      fullWidth
      onClick={handleClick}
      disabled={disabled || isLoading}
      startIcon={icon}
      sx={{
        textTransform: 'none',
        borderColor: 'divider',
        color: 'text.primary',
        '&:hover': {
          borderColor: 'primary.main',
          backgroundColor: 'action.hover',
        },
      }}>
      {buttonText}
    </Button>
  );
}
