import { getRouteApi } from '@tanstack/react-router'
import { Avatar, AvatarFallback } from 'app/components/ui/avatar'
import { Button } from 'app/components/ui/button'
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from 'app/components/ui/dropdown-menu'
import {
  Tooltip,
  TooltipContent,
  TooltipProvider,
  TooltipTrigger,
} from 'app/components/ui/tooltip'
import { LogOut, User } from 'lucide-react'
import { LinkButton } from 'shared/ui/LinkButton'

const routeApi = getRouteApi('__root__')

export function AccountMenu() {
  const {
    auth: { user, logout },
  } = routeApi.useRouteContext()
  const navigate = routeApi.useNavigate()

  if (!user) return null
  return (
    <DropdownMenu>
      <TooltipProvider>
        <Tooltip>
          <TooltipTrigger asChild>
            <DropdownMenuTrigger asChild>
              <Button variant='ghost' size='icon' className='ml-2 rounded-full'>
                <Avatar className='size-8'>
                  <AvatarFallback>
                    {user.username.charAt(0).toUpperCase()}
                  </AvatarFallback>
                </Avatar>
              </Button>
            </DropdownMenuTrigger>
          </TooltipTrigger>
          <TooltipContent>Account settings</TooltipContent>
        </Tooltip>
      </TooltipProvider>
      <DropdownMenuContent align='end'>
        <DropdownMenuItem asChild>
          <LinkButton
            to='/profile'
            variant='ghost'
            className='w-full justify-start'
          >
            <User className='size-4' />
            Profile
          </LinkButton>
        </DropdownMenuItem>
        <DropdownMenuSeparator />
        <DropdownMenuItem
          onClick={() => {
            logout().finally(() => {
              navigate({ to: '/' })
            })
          }}
        >
          <LogOut className='size-4' />
          Logout
        </DropdownMenuItem>
      </DropdownMenuContent>
    </DropdownMenu>
  )
}
