type BaseFormProps = React.ComponentProps<'form'>

export function Form({ children, className, ...props }: BaseFormProps) {
  return (
    <form
      noValidate
      className={['flex max-w-110 flex-col justify-center px-5', className]
        .filter(Boolean)
        .join(' ')}
      {...props}
    >
      {children}
    </form>
  )
}
