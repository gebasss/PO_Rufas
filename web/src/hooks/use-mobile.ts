import * as React from 'react'

const MOBILE_BREAKPOINT = 1280

/**
 * Indica se a janela é estreita (a barra lateral vira uma gaveta).
 *
 * Começa como `false` e só mede depois da montagem: o site é exportado como HTML estático, e ler `window` no
 * estado inicial gerava divergência de hidratação (erro #418 do React) em telas estreitas.
 */
export function useIsMobile() {
  const [isMobile, setIsMobile] = React.useState(false)

  React.useEffect(() => {
    const mql = window.matchMedia(`(max-width: ${MOBILE_BREAKPOINT - 1}px)`)

    const onChange = () => setIsMobile(window.innerWidth < MOBILE_BREAKPOINT)

    onChange()
    mql.addEventListener('change', onChange)

    return () => mql.removeEventListener('change', onChange)
  }, [])

  return isMobile
}
