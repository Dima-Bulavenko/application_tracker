import { getRouteApi } from '@tanstack/react-router'
import { Button } from 'app/components/ui/button'
import { Loader2, Trash2 } from 'lucide-react'
import { useState } from 'react'
import { useDeleteUser } from '../hooks/useDeleteUser'
import { DeleteAccountDialog } from './DeleteAccountDialog'

const routeApi = getRouteApi('__root__')

export function DeleteAccountButton() {
  const [open, setOpen] = useState(false)
  const [isDeleting, setIsDeleting] = useState(false)
  const deleteUser = useDeleteUser()
  const navigate = routeApi.useNavigate()

  const handleOpen = () => setOpen(true)
  const handleClose = () => {
    if (!isDeleting) setOpen(false)
  }

  const handleConfirm = async () => {
    setIsDeleting(true)
    try {
      await deleteUser()
      navigate({ to: '/' })
    } catch (error) {
      console.error('Failed to delete account:', error)
    } finally {
      setIsDeleting(false)
      handleClose()
    }
  }

  return (
    <>
      <Button variant='destructive' disabled={isDeleting} onClick={handleOpen}>
        {isDeleting ? (
          <Loader2 className='size-4 animate-spin' />
        ) : (
          <Trash2 className='size-4' />
        )}
        Delete Account
      </Button>
      <DeleteAccountDialog
        open={open}
        onClose={handleClose}
        onConfirm={handleConfirm}
        isDeleting={isDeleting}
      />
    </>
  )
}
