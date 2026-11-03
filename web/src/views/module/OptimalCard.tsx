'use client'

import { AlertTriangleIcon, CheckCircle2Icon, SparklesIcon, SquareIcon } from 'lucide-react'

import { feedTitle } from '@/components/FeedPicker'
import { NumberInput, KpiCard } from '@/components/shared'
import { Segmented } from '@/components/Segmented'
import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Label } from '@/components/ui/label'
import { Progress } from '@/components/ui/progress'
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table'
import { nf, signedPct, usd } from '@/lib/format'
import { cn } from '@/lib/utils'
import type { Feed, ModuleOptimization, OptimizationResolution } from '@/lib/types'

import { MAX_SEEDS, RESOLUTIONS } from './model'
import { ConstraintTable } from './ResultCard'

const REGIME: Record<string, string> = {
  sem_desconto: 'TDN% abaixo de 60 (sem desconto de ingestão)',
  com_desconto: 'TDN% a partir de 60 (com desconto de ingestão)'
}

interface Props {
  library: Record<number, Feed>
  result: ModuleOptimization | null
  /** O resultado mostrado não corresponde mais às entradas atuais. */
  stale: boolean
  running: boolean
  progress: { done: number; total: number } | null
  error: string | null
  blockers: string[]
  resolution: OptimizationResolution
  seeds: number
  onResolution: (value: OptimizationResolution) => void
  onSeeds: (value: number) => void
  onRun: () => void
  onCancel: () => void
}

export default function OptimalCard({
  library,
  result,
  stale,
  running,
  progress,
  error,
  blockers,
  resolution,
  seeds,
  onResolution,
  onSeeds,
  onRun,
  onCancel
}: Props) {
  const name = (id: string | number) => (library[Number(id)] ? feedTitle(library[Number(id)]) : `Alimento ${id}`)
  const diet = result?.diet
  const rufas = result?.rufas
  const bestRun = rufas?.runs.find(run => run.seed === rufas.best_seed) ?? null
  const rows = diet
    ? [...new Set([...Object.keys(diet.amounts), ...Object.keys(bestRun?.amounts ?? {})])]
        .map(id => ({ id, lp: diet.amounts[id] ?? 0, rufas: bestRun?.amounts[id] ?? 0 }))
        .sort((a, b) => b.lp - a.lp || b.rufas - a.rufas)
    : []
  const shadowLabel = (item: { id: string; label: string }) => {
    const limit = item.id.match(/^limit_(ge|le)_(\d+)$/)

    return limit ? `Limite ${limit[1] === 'ge' ? 'mínimo' : 'máximo'} de ${name(limit[2])}` : item.label
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>Dieta ótima</CardTitle>
        <CardDescription>
          A dieta de menor custo entre os alimentos da tabela que atende às mesmas restrições. Com o consumo, o TDN% e o %
          de concentrado fixos o problema é linear; um programa linear é resolvido em uma grade desses valores e refinado
          em torno do melhor ponto. A dieta é conferida com as funções originais do RuFaS e comparada com o otimizador do
          RuFaS (SLSQP), que parte de um ponto aleatório.
        </CardDescription>
      </CardHeader>
      <CardContent className='space-y-6'>
        <div className='space-y-3'>
          <div className='flex flex-wrap items-end gap-4'>
            <div className='flex flex-col justify-end gap-1.5'>
              <Label>Resolução da busca</Label>
              <Segmented
                label='Resolução da busca'
                value={resolution}
                options={RESOLUTIONS}
                onChange={onResolution}
                disabled={running}
              />
            </div>
            <div className='flex flex-col justify-end gap-1.5'>
              <Label htmlFor='optimal-seeds'>Execuções do RuFaS (0 a {MAX_SEEDS})</Label>
              <NumberInput id='optimal-seeds' className='w-28' step={1} min={0} value={seeds} onChange={onSeeds} />
            </div>
            {running ? (
              <Button variant='outline' onClick={onCancel}>
                <SquareIcon /> Cancelar
              </Button>
            ) : (
              <Button onClick={onRun} disabled={blockers.length > 0}>
                <SparklesIcon /> Calcular dieta ótima
              </Button>
            )}
          </div>
          {blockers.length > 0 && (
            <ul className='text-muted-foreground list-disc space-y-0.5 pl-4 text-sm'>
              {blockers.map(blocker => (
                <li key={blocker}>{blocker}</li>
              ))}
            </ul>
          )}
          {running && (
            <div className='space-y-1.5' role='status' aria-live='polite'>
              <Progress value={progress?.total ? (100 * progress.done) / progress.total : null} />
              <p className='text-muted-foreground text-xs'>
                {progress?.total ? `${progress.done} de ${progress.total} passos` : 'Na fila…'}
              </p>
            </div>
          )}
          {result && stale && !running && (
            <p className='text-muted-foreground text-sm' role='status'>
              As entradas mudaram desde o último cálculo. Clique em Calcular dieta ótima para atualizar.
            </p>
          )}
        </div>

        {error && (
          <Alert variant='destructive'>
            <AlertTriangleIcon />
            <AlertTitle>Não foi possível calcular</AlertTitle>
            <AlertDescription>{error.split('\n')[0]}</AlertDescription>
          </Alert>
        )}

        {result?.status === 'infeasible' && (
          <Alert>
            <AlertTriangleIcon />
            <AlertTitle>Sem dieta viável</AlertTitle>
            <AlertDescription>{result.message}</AlertDescription>
          </Alert>
        )}

        {result && diet && (
          <div className={cn('space-y-6 transition-opacity', (running || stale) && 'opacity-60')}>
            {result.warnings.length > 0 && (
              <Alert>
                <AlertTriangleIcon />
                <AlertTitle>Avisos</AlertTitle>
                <AlertDescription>
                  <ul className='list-disc space-y-1 pl-4'>
                    {[...new Set(result.warnings)].map(warning => (
                      <li key={warning}>{warning}</li>
                    ))}
                  </ul>
                </AlertDescription>
              </Alert>
            )}

            <div className='grid grid-cols-2 gap-3 lg:grid-cols-4'>
              <KpiCard label='Custo' value={usd(diet.cost, 2)} hint='por vaca e por dia' />
              <KpiCard label='Custo por kg de MS' value={usd(diet.cost_per_kg, 3)} />
              <KpiCard label='Consumo de MS' value={`${nf(diet.scalars.dmi, 2)} kg/dia`} />
              <KpiCard
                label='TDN · concentrado'
                value={`${nf(diet.scalars.tdn_percentage, 1)}% · ${nf(diet.scalars.concentrate_percentage, 1)}%`}
                hint={REGIME[diet.regime]}
              />
            </div>

            <p className='flex flex-wrap items-center gap-2 text-sm'>
              {diet.verified ? (
                <Badge variant='secondary'>
                  <CheckCircle2Icon aria-hidden /> Confere com o RuFaS
                </Badge>
              ) : (
                <Badge variant='outline' className='bg-destructive/10 text-destructive'>
                  <AlertTriangleIcon aria-hidden /> Viola restrições do RuFaS
                </Badge>
              )}
              <span className='text-muted-foreground'>
                {diet.verified
                  ? 'Todas as restrições originais são atendidas.'
                  : `Violadas: ${diet.evaluation.violated.join(', ')}.`}{' '}
                Busca: {result.search.feasible_points} pontos viáveis de {result.search.points} testados, em{' '}
                {nf(result.search.seconds, 1)} s.
              </span>
            </p>

            <div className='space-y-2'>
              <h3 className='text-muted-foreground text-xs font-medium tracking-wider uppercase'>Ração</h3>
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead>Alimento</TableHead>
                    <TableHead className='text-right'>Dieta ótima (kg MS/dia)</TableHead>
                    <TableHead className='text-right'>% da dieta</TableHead>
                    {bestRun && <TableHead className='text-right'>Melhor do RuFaS (kg MS/dia)</TableHead>}
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {rows.map(row => (
                    <TableRow key={row.id}>
                      <TableCell className='text-sm leading-snug'>{name(row.id)}</TableCell>
                      <TableCell className='text-right tabular-nums'>{nf(row.lp, 2)}</TableCell>
                      <TableCell className='text-right tabular-nums'>{nf((100 * row.lp) / diet.scalars.dmi, 1)}%</TableCell>
                      {bestRun && <TableCell className='text-right tabular-nums'>{nf(row.rufas, 2)}</TableCell>}
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </div>

            {rufas && (
              <div className='space-y-3'>
                <h3 className='text-muted-foreground text-xs font-medium tracking-wider uppercase'>
                  Comparação com o otimizador do RuFaS
                </h3>
                {rufas.cost_min == null ? (
                  <p className='text-muted-foreground text-sm'>
                    Nenhuma das {rufas.n_runs} execuções do RuFaS convergiu para uma dieta viável.
                  </p>
                ) : (
                  <div className='grid grid-cols-2 gap-3 lg:grid-cols-4'>
                    <KpiCard
                      label='Dieta ótima (LP) em relação ao RuFaS'
                      value={signedPct(rufas.lp_gap_pct)}
                      hint={(rufas.lp_gap_pct ?? 0) > 0 ? 'o RuFaS achou custo menor' : 'o LP é igual ou mais barato'}
                    />
                    <KpiCard label='Melhor custo do RuFaS' value={usd(rufas.cost_min, 4)} />
                    <KpiCard label='Mediana do RuFaS' value={usd(rufas.cost_median, 4)} />
                    <KpiCard
                      label='Execuções viáveis'
                      value={`${rufas.n_success} de ${rufas.n_runs}`}
                      hint={`pior custo ${usd(rufas.cost_max, 4)}`}
                    />
                  </div>
                )}
                <Table>
                  <TableHeader>
                    <TableRow>
                      <TableHead>Semente</TableHead>
                      <TableHead>Resultado</TableHead>
                      <TableHead className='text-right'>Custo (US$/dia)</TableHead>
                      <TableHead className='text-right'>Iterações</TableHead>
                      <TableHead className='text-right'>Tempo (s)</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {rufas.runs.map(run => (
                      <TableRow key={run.seed}>
                        <TableCell className='tabular-nums'>{run.seed}</TableCell>
                        <TableCell>
                          {run.success && run.feasible ? (
                            <Badge variant='secondary'>
                              <CheckCircle2Icon aria-hidden /> Viável
                            </Badge>
                          ) : (
                            <Badge variant='outline' className='bg-destructive/10 text-destructive'>
                              <AlertTriangleIcon aria-hidden /> {run.success ? 'Viola restrições' : 'Não convergiu'}
                            </Badge>
                          )}
                        </TableCell>
                        <TableCell className='text-right tabular-nums'>{nf(run.cost, 4)}</TableCell>
                        <TableCell className='text-right tabular-nums'>{run.iterations}</TableCell>
                        <TableCell className='text-right tabular-nums'>{nf(run.seconds, 2)}</TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </div>
            )}

            <div className='space-y-3'>
              <h3 className='text-muted-foreground text-xs font-medium tracking-wider uppercase'>
                Restrições da dieta ótima
              </h3>
              <ConstraintTable diet={diet.evaluation} />
            </div>

            {result.shadow_prices && result.shadow_prices.length > 0 && (
              <div className='space-y-2'>
                <h3 className='text-muted-foreground text-xs font-medium tracking-wider uppercase'>Preços-sombra</h3>
                <Table>
                  <TableHeader>
                    <TableRow>
                      <TableHead>Restrição ativa</TableHead>
                      <TableHead className='text-right'>Variação do custo (US$/dia por unidade)</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {result.shadow_prices.map(item => (
                      <TableRow key={item.id}>
                        <TableCell className='text-sm'>{shadowLabel(item)}</TableCell>
                        <TableCell className='text-right tabular-nums'>{nf(item.value, 4)}</TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
                <p className='text-muted-foreground text-xs'>
                  Quanto o custo diário mudaria se a exigência (ou o limite) subisse uma unidade, na unidade da restrição.
                  Valem perto da dieta ótima e com o consumo, o TDN% e o % de concentrado fixos. Positivo = exigir mais
                  custa mais; negativo = afrouxar um teto economiza.
                </p>
              </div>
            )}
          </div>
        )}
      </CardContent>
    </Card>
  )
}
