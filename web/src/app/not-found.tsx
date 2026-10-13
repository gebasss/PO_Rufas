import Link from 'next/link'

export default function NotFound() {
  return (
    <div className='flex min-h-[50vh] flex-col items-center justify-center gap-3 text-center'>
      <h1 className='text-2xl font-semibold'>Página não encontrada</h1>
      <Link href='/' className='text-primary underline-offset-4 hover:underline'>
        Voltar ao início
      </Link>
    </div>
  )
}
