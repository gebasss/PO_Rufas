import { AlertTriangleIcon, CheckCircle2Icon } from 'lucide-react'

import { Badge } from '@/components/ui/badge'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table'
import { nf, signedPct } from '@/lib/format'
import type { BalanceRow } from '@/lib/types'

const digits = (value: number) => (Math.abs(value) < 10 ? 2 : 1)
const fmt = (value: number | null | undefined) => (value == null ? '—' : nf(value, digits(value)))
const signed = (value: number) => (Math.abs(value) < 0.005 ? nf(0, 2) : `${value > 0 ? '+' : ''}${nf(value, digits(value))}`)

const STATUS: Record<BalanceRow['status'], string> = { ok: 'Atende', deficit: 'Déficit', fora: 'Fora da faixa' }

function Status({ status }: { status: BalanceRow['status'] }) {
  return status === 'ok' ? (
    <Badge variant='secondary'>
      <CheckCircle2Icon aria-hidden /> {STATUS[status]}
    </Badge>
  ) : (
    <Badge variant='outline' className='bg-destructive/10 text-destructive'>
      <AlertTriangleIcon aria-hidden /> {STATUS[status]}
    </Badge>
  )
}

/** Como ler a coluna "Diferença" de cada tipo de linha (convenções do RuFaS). */
const DIFFERENCE_HINT: Record<BalanceRow['kind'], string> = {
  surplus: 'oferta − exigência',
  range: '0 = dentro da faixa',
  floor: '% da ração − mínimo',
  ceiling: 'máximo − % da ração'
}

/** Tabela do balanço (e nota de leitura); o gráfico de diferenças em % é montado no cartão que a usa. */
export function BalanceTable({ rows }: { rows: BalanceRow[] }) {
  return (
    <div className='space-y-3'>
      <Table>
        <TableHeader>
          <TableRow>
            <TableHead className='min-w-56'>Nutriente</TableHead>
            <TableHead className='text-right'>Exigência</TableHead>
            <TableHead className='text-right'>Oferta</TableHead>
            <TableHead className='text-right'>Diferença (média)</TableHead>
            <TableHead className='text-right'>Pior intervalo</TableHead>
            <TableHead>Estado</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {rows.map(row => (
            <TableRow key={row.id}>
              <TableCell>
                <span className='block text-sm leading-snug'>{row.label}</span>
                <span className='text-muted-foreground block text-xs'>
                  {row.unit} · {DIFFERENCE_HINT[row.kind]}
                </span>
                {row.note && <span className='text-muted-foreground block text-xs'>{row.note}</span>}
              </TableCell>
              <TableCell className='text-right tabular-nums'>{fmt(row.requirement)}</TableCell>
              <TableCell className='text-right tabular-nums'>{fmt(row.supply)}</TableCell>
              <TableCell className='text-right tabular-nums'>
                {signed(row.difference)}
                {row.margin_pct != null && (
                  <span className='text-muted-foreground block text-xs'>{signedPct(row.margin_pct, 1)}</span>
                )}
              </TableCell>
              <TableCell className='text-right tabular-nums'>{signed(row.worst_difference)}</TableCell>
              <TableCell>
                <Status status={row.status} />
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
      <p className='text-muted-foreground text-xs'>
        Na proteína metabolizável e no consumo, o RuFaS só informa se a ração está na faixa aceita (a oferta exata não
        aparece). A exigência de fósforo é a maior entre a da vaca e a do processo.
      </p>
    </div>
  )
}

export default function BalanceCard({ rows }: { rows: BalanceRow[] }) {
  return (
    <Card>
      <CardHeader>
        <CardTitle>Balanço nutricional</CardTitle>
        <CardDescription>
          O que a ração oferece contra o que a vaca exige, calculado pelo próprio RuFaS a cada intervalo de 30 dias e
          resumido pela média e pelo pior intervalo. Positivo = sobra; negativo = falta.
        </CardDescription>
      </CardHeader>
      <CardContent>
        <BalanceTable rows={rows} />
      </CardContent>
    </Card>
  )
}
