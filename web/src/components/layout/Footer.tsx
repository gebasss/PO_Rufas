const Footer = () => {
  return (
    <footer>
      <div className='text-muted-foreground mx-auto flex max-w-360 flex-wrap items-center justify-between gap-x-6 gap-y-1 px-4 py-3 text-xs sm:px-6'>
        <p>
          Simulador:{' '}
          <a
            href='https://github.com/RuminantFarmSystems/RuFaS'
            target='_blank'
            rel='noopener noreferrer'
            className='text-primary hover:underline'
          >
            RuFaS
          </a>{' '}
          v1.0.6 (GPLv3) · Exigências e composição: NRC (2001) · Preços ilustrativos, não são cotações.
        </p>
        <p>Interface adaptada do template AdminCN (shadcn/studio, licença MIT).</p>
      </div>
    </footer>
  )
}

export default Footer
