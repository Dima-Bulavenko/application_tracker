import { getRouteApi } from '@tanstack/react-router'
import { AccountMenu } from 'features/user/ui/AccountMenu'
import { ColorModeToggler } from 'shared/ui/ColorModeToggler'
import { LinkButton } from 'shared/ui/LinkButton'

const routeApi = getRouteApi('__root__')

export function Header() {
  const {
    auth: { user },
  } = routeApi.useRouteContext()
  return (
    <header className='sticky top-0 z-50 w-full border-b bg-background'>
      <div className='flex h-16 items-center gap-1 px-4'>
        <LinkButton to={user ? '/dashboard' : '/'} variant='ghost'>
          <img
            src='/logo.svg'
            alt='Application Tracker'
            className='h-[30px] w-[70px]'
          />
        </LinkButton>
        <div className='flex-1' />

        <div className='flex items-center gap-1'>
          {user ? (
            <AccountMenu />
          ) : (
            <>
              <LinkButton size='sm' variant='ghost' to='/sign-in'>
                Login
              </LinkButton>
              <LinkButton size='sm' to='/register'>
                Register
              </LinkButton>
            </>
          )}
        </div>

        <ColorModeToggler />
      </div>
    </header>
  )
}

export default Header
