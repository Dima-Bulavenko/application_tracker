import {
  Card,
  CardContent,
  CardFooter,
  CardHeader,
  CardTitle,
} from 'app/components/ui/card'
import { Separator } from 'app/components/ui/separator'
import { Link } from 'shared/ui/Link'

export interface AuthPageProps {
  title: string
  subtitle?: string
  children: React.ReactNode
  footerText?: string
  footerLinkText?: string
  footerTo?: string
}

export function AuthPage({
  title,
  subtitle,
  children,
  footerText,
  footerLinkText,
  footerTo,
}: AuthPageProps) {
  return (
    <section className='grid min-h-dvh place-items-center px-2 py-8'>
      <Card className='w-full max-w-[480px]'>
        <CardHeader>
          <CardTitle className='text-2xl'>{title}</CardTitle>
          {subtitle && (
            <p className='text-sm text-muted-foreground'>{subtitle}</p>
          )}
        </CardHeader>
        <CardContent className='space-y-3'>{children}</CardContent>
        {(footerText || (footerLinkText && footerTo)) && (
          <CardFooter className='flex-col gap-3'>
            <Separator />
            <p className='text-center text-sm text-muted-foreground'>
              {footerText}{' '}
              {footerLinkText && footerTo && (
                <Link
                  to={footerTo}
                  className='underline-offset-4 hover:underline'
                >
                  {footerLinkText}
                </Link>
              )}
            </p>
          </CardFooter>
        )}
      </Card>
    </section>
  )
}
