type BaseFormProps = React.ComponentProps<'form'>

export function Form({ children, className, ...props }: BaseFormProps) {
  return (
    <form
      noValidate
      className={[
        'mx-auto flex max-w-[440px] flex-col justify-center p-6',
        className,
      ]
        .filter(Boolean)
        .join(' ')}
      {...props}
    >
      {children}
    </form>
  )
}
