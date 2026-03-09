import { getRouteApi } from '@tanstack/react-router'
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
} from 'app/components/ui/card'
import { LinkButton } from 'shared/ui/LinkButton'

const roteApi = getRouteApi('__root__')

export function HomePage() {
  const {
    auth: { isAuthenticated },
  } = roteApi.useRouteContext()
  return (
    <div className='space-y-16 py-6'>
      {/* Hero Section */}
      <section className='text-center'>
        <h1 className='text-4xl font-bold tracking-tight'>
          Application Tracker
        </h1>
        <p className='mx-auto mt-2 max-w-[720px] text-lg text-muted-foreground'>
          Track and manage all your job applications in one organized workspace.
          Stay on top of every stage—from submission to interviews and offers.
        </p>
        <div className='mt-4 flex justify-center gap-2'>
          {isAuthenticated ? (
            <LinkButton to='/dashboard'>Go to Dashboard</LinkButton>
          ) : (
            <>
              <LinkButton to='/register'>Get Started</LinkButton>
              <LinkButton to='/sign-in' variant='outline'>
                Sign In
              </LinkButton>
            </>
          )}
        </div>
      </section>

      <section className='mx-auto max-w-5xl px-2'>
        <div className='grid gap-4 sm:grid-cols-2 md:grid-cols-3'>
          {[
            {
              title: 'Centralized Tracking',
              body: 'Keep every application, company detail, and note in one place for quick reference and decision making.',
            },
            {
              title: 'Status Management',
              body: 'Monitor progress through each stage and never lose track of next steps or deadlines.',
            },
            {
              title: 'Actionable Insights',
              body: 'Coming soon: analytics to help you understand response rates and optimize your search.',
            },
          ].map((feature) => (
            <Card key={feature.title} className='h-full'>
              <CardHeader>
                <CardTitle className='text-lg'>{feature.title}</CardTitle>
              </CardHeader>
              <CardContent>
                <p className='text-sm text-muted-foreground'>{feature.body}</p>
              </CardContent>
            </Card>
          ))}
        </div>
      </section>

      {/* Auth Prompt */}
      {!isAuthenticated && (
        <section className='text-center'>
          <p className='mb-2 text-muted-foreground'>
            Create a free account to start organizing your applications.
          </p>
          <LinkButton to='/register'>Create Account</LinkButton>
        </section>
      )}
    </div>
  )
}
