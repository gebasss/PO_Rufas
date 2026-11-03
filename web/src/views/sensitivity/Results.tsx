'use client'

import { useMemo, useState } from 'react'

import { GaugeIcon, ListIcon, SlidersHorizontalIcon, TrendingDownIcon, TrendingUpIcon, WaypointsIcon } from 'lucide-react'

import { DivergingBars, HighlightBars, ScatterPlot } from '@/components/charts'
import ChartCard from '@/components/ChartCard'
import ExportButtons from '@/components/ExportButtons'
import { heat, KpiCard } from '@/components/shared'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { Tabs, TabsList, TabsPanel, TabsTab } from '@/components/ui/tabs'
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table'
import { shortDate } from '@/lib/history'
import { nf, shortName, usd } from '@/lib/format'
import type { RunMeta, SensResult } from '@/lib/types'

interface Props {
  result: SensResult
  /** Os fatores ou a simulação mudaram desde esta análise. */
  stale?: boolean
  /** Simulação-base (D3): vira a linha de referência dos gráficos e o delta da melhor margem. */
  base?: RunMeta | null
  /** Período simulado, para só comparar com a base quando ele é o mesmo (a margem cresce com os anos). */
  years?: number
}

/** Números do eixo vertical em milhares ("450 mil"), mais curtos que o rótulo com US$. */
const thousands = (value: number) => `${nf(value / 1000, 0)} mil`

const signed = (value: number) => `${value > 0 ? '+' : ''}${nf(value, 2)}`

/** Contagem de cenários por faixa de margem (raiz do número de cenários, de 3 a 12 faixas). */
function histogram(values: number[]) {
  const lo = Math.min(...values)
  const hi = Math.max(...values)
  const bins = Math.min(12, Math.max(3, Math.round(Math.sqrt(values.length))))
  const width = (hi - lo) / bins || 1
  const counts = Array.from({ length: bins }, (_, i) => ({ from: lo + i * width, to: lo + (i + 1) * width, count: 0 }))

  for (const value of values) counts[Math.min(bins - 1, Math.floor((value - lo) / width))].count += 1

  return counts
}

export default function SensResults({ result, stale = false, base = null, years }: Props) {
  const names = useMemo(() => Object.fromEntries(result.feeds.map(f => [String(f.id), shortName(f.label, 26)])), [result.feeds])
  const factorColumns = result.columns.filter(c => c !== 'Res')
  const okRows = result.rows.filter(r => r.Res !== null)
  const margins = okRows.map(r => r.Res as number)
  const best = okRows.reduce<(typeof okRows)[number] | null>((a, r) => (a === null || (r.Res as number) > (a.Res as number) ? r : a), null)
  const worst = okRows.reduce<(typeof okRows)[number] | null>((a, r) => (a === null || (r.Res as number) < (a.Res as number) ? r : a), null)
  const [factor, setFactor] = useState(factorColumns[0] ?? '')

  const baseMargin = base && typeof base.summary.margem === 'number' && (years === undefined || base.summary.years === years) ? base.summary.margem : null
  const bestDelta = best && baseMargin ? (((best.Res as number) - baseMargin) / Math.abs(baseMargin)) * 100 : undefined

  const bars = okRows.map(r => ({ name: r.cenario, value: r.Res as number }))
  const bins = margins.length ? histogram(margins) : []
  const bestBin = best ? bins.findIndex(b => (best.Res as number) >= b.from && (best.Res as number) <= b.to) : -1
  const histogramData = bins.map((b, i) => ({ name: `${usd(b.from, 0)}`, value: b.count, to: b.to, index: i }))

  const effects = result.effects
    .filter(e => e.spearman !== null)
    .map(e => ({ name: shortName(e.fator, 26), value: e.spearman as number }))
    .sort((a, b) => Math.abs(b.value) - Math.abs(a.value))
  const topEffect = effects[0]

  const scatter = okRows.map(r => ({ name: r.cenario, x: Number(r[factor]), y: r.Res as number })).filter(p => Number.isFinite(p.x))
  const bestRation = best?.ration
    ? Object.entries(best.ration)
        .filter(([, kg]) => kg > 1e-3)
        .sort((a, b) => b[1] - a[1])
        .slice(0, 8)
        .map(([id, kg]) => ({ name: names[id] ?? id, value: kg }))
    : []

  const [min, max] = [Math.min(...margins), Math.max(...margins)]

  const scenarioTable = (
    <Table>
      <TableHeader>
        <TableRow>
          <TableHead />
          {factorColumns.map(c => (
            <TableHead key={c} className='text-right'>
              {shortName(c, 24)}
            </TableHead>
          ))}
          <TableHead className='text-right'>Res (US$)</TableHead>
          <TableHead className='text-right'>US$/vaca/dia</TableHead>
          <TableHead className='text-right'>Leite perdido</TableHead>
          <TableHead>Ração (kg MS/vaca/dia)</TableHead>
        </TableRow>
      </TableHeader>
      <TableBody>
        {result.rows.map(row => (
          <TableRow key={row.cenario} data-state={best && row.cenario === best.cenario ? 'selected' : undefined}>
            <TableCell className='font-medium'>{row.cenario}</TableCell>
            {factorColumns.map(c => (
              <TableCell key={c} className='text-right tabular-nums'>
                {nf(row[c] as number, 3)}
              </TableCell>
            ))}
            <TableCell className='text-right font-semibold tabular-nums' style={row.Res === null ? undefined : heat(row.Res, min, max)} title={row.erro}>
              {row.Res === null ? <span className='text-destructive'>falhou</span> : usd(row.Res)}
            </TableCell>
            <TableCell className='text-right tabular-nums'>{row.custo_vaca_dia !== undefined ? nf(row.custo_vaca_dia, 2) : '—'}</TableCell>
            <TableCell className='text-right tabular-nums'>
              {(row.reducao_leite ?? 0) > 0.005 ? <span className='text-warning-text'>−{nf(row.reducao_leite, 2)}</span> : '—'}
            </TableCell>
            <TableCell className='text-muted-foreground max-w-80 text-xs'>
              {row.ration
                ? Object.entries(row.ration)
                    .sort((a, b) => b[1] - a[1])
                    .slice(0, 4)
                    .map(([id, kg]) => `${names[id] ?? id} ${nf(kg, 1)}`)
                    .join(' · ')
                : row.erro}
            </TableCell>
          </TableRow>
        ))}
      </TableBody>
    </Table>
  )

  return (
    <div className='min-w-0 scroll-mt-24'>
      <Tabs defaultValue='overview'>
        <div className='flex flex-wrap items-center justify-between gap-3'>
          <TabsList>
            <TabsTab value='overview'>
              <GaugeIcon /> Visão geral
            </TabsTab>
            <TabsTab value='factors'>
              <SlidersHorizontalIcon /> Fatores
            </TabsTab>
            <TabsTab value='scenarios'>
              <ListIcon /> Cenários
            </TabsTab>
          </TabsList>
          <ExportButtons screen='sensitivity' data={result} meta={{ standard: 'NRC 2001' }} />
        </div>

        <div className={stale ? 'space-y-6 opacity-60 transition-opacity' : 'space-y-6 transition-opacity'}>
          {stale && (
            <p className='text-muted-foreground text-sm' role='status'>
              Os fatores ou os parâmetros mudaram desde esta análise. Clique em Executar para atualizá-la.
            </p>
          )}

          <TabsPanel value='overview'>
            {best && worst ? (
              <div className='grid gap-3 sm:grid-cols-2 2xl:grid-cols-4'>
                <KpiCard
                  tone='primary'
                  icon={TrendingUpIcon}
                  label={`Melhor margem (${best.cenario})`}
                  value={usd(best.Res as number, 0)}
                  delta={bestDelta}
                  hint={bestDelta !== undefined ? 'vs. simulação-base' : undefined}
                  trend={margins}
                />
                <KpiCard icon={TrendingDownIcon} color='destructive' label={`Pior margem (${worst.cenario})`} value={usd(worst.Res as number, 0)} />
                <KpiCard
                  icon={WaypointsIcon}
                  color='violet'
                  label='Amplitude entre o melhor e o pior'
                  value={usd((best.Res as number) - (worst.Res as number), 0)}
                  hint={`${nf((100 * ((best.Res as number) - (worst.Res as number))) / Math.abs(best.Res as number), 1)}% da melhor margem`}
                />
                <KpiCard
                  icon={ListIcon}
                  color='info'
                  label='Cenários com resultado'
                  value={`${okRows.length} de ${result.rows.length}`}
                  hint={okRows.length < result.rows.length ? 'alguns falharam; veja a aba Cenários' : undefined}
                />
              </div>
            ) : (
              <Card>
                <CardContent className='text-muted-foreground py-10 text-center text-sm'>Nenhum cenário terminou com resultado.</CardContent>
              </Card>
            )}

            {best && (
              <div className='grid gap-6 2xl:grid-cols-2'>
                <ChartCard
                  title='Margem por cenário'
                  description={
                    <>
                      US$ sobre o custo de alimentação; o cenário ótimo em verde vivo
                      {baseMargin !== null && base ? ` e a linha tracejada é a simulação-base (${shortDate(base.created)})` : ''}.
                    </>
                  }
                  chart={
                    <HighlightBars
                      data={bars}
                      highlight={best.cenario}
                      format={value => usd(value, 0)}
                      axisFormat={thousands}
                      height={260}
                      reference={baseMargin ?? undefined}
                      referenceLabel={baseMargin !== null ? 'Base' : undefined}
                    />
                  }
                  table={
                    <Table>
                      <TableHeader>
                        <TableRow>
                          <TableHead>Cenário</TableHead>
                          <TableHead className='text-right'>Margem (US$)</TableHead>
                        </TableRow>
                      </TableHeader>
                      <TableBody>
                        {bars.map(row => (
                          <TableRow key={row.name} data-state={row.name === best.cenario ? 'selected' : undefined}>
                            <TableCell>{row.name}</TableCell>
                            <TableCell className='text-right tabular-nums'>{usd(row.value, 0)}</TableCell>
                          </TableRow>
                        ))}
                      </TableBody>
                    </Table>
                  }
                />
                <ChartCard
                  title='Distribuição das margens'
                  description='Quantos cenários caem em cada faixa de margem; a faixa do cenário ótimo em verde vivo.'
                  chart={<HighlightBars data={histogramData} highlight={histogramData[bestBin]?.name} format={value => String(value)} height={260} />}
                  table={
                    <Table>
                      <TableHeader>
                        <TableRow>
                          <TableHead>Faixa de margem</TableHead>
                          <TableHead className='text-right'>Cenários</TableHead>
                        </TableRow>
                      </TableHeader>
                      <TableBody>
                        {histogramData.map(row => (
                          <TableRow key={row.name}>
                            <TableCell>
                              {row.name} a {usd(row.to, 0)}
                            </TableCell>
                            <TableCell className='text-right tabular-nums'>{row.value}</TableCell>
                          </TableRow>
                        ))}
                      </TableBody>
                    </Table>
                  }
                />
              </div>
            )}

            {bestRation.length > 0 && best && (
              <ChartCard
                title={`Ração do cenário ótimo (${best.cenario})`}
                description={`kg de matéria seca por vaca por dia; fatores: ${factorColumns.map(c => `${shortName(c, 22)} ${nf(best[c] as number, 3)}`).join(' · ')}.`}
                chart={<HighlightBars layout='vertical' data={bestRation} highlight={bestRation[0].name} format={value => nf(value, 1)} height={Math.max(200, bestRation.length * 38 + 30)} />}
              />
            )}
          </TabsPanel>

          <TabsPanel value='factors'>
            <ChartCard
              title='Efeito de cada fator sobre a margem'
              description='Correlação de Spearman entre o fator e a margem (−1 a +1), do maior para o menor efeito. Verde: subir o fator aumenta a margem; vermelho: reduz.'
              chart={
                effects.length > 0 ? (
                  <DivergingBars data={effects} format={signed} domain={[-1, 1]} height={Math.max(200, effects.length * 44 + 30)} />
                ) : (
                  <p className='text-muted-foreground py-8 text-center text-sm'>Os fatores não variaram o suficiente para calcular o efeito.</p>
                )
              }
              table={
                <Table>
                  <TableHeader>
                    <TableRow>
                      <TableHead>Fator</TableHead>
                      <TableHead className='text-right'>Spearman</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {effects.map(row => (
                      <TableRow key={row.name}>
                        <TableCell>{row.name}</TableCell>
                        <TableCell className='text-right tabular-nums'>{signed(row.value)}</TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              }
            />
            {factorColumns.length > 0 && best && (
              <ChartCard
                title='Margem em função de um fator'
                description={
                  <span className='flex flex-wrap items-center gap-2'>
                    Um ponto por cenário; o ótimo em verde vivo.
                    <Select value={factor} items={factorColumns.map(c => ({ value: c, label: c }))} onValueChange={v => v && setFactor(v)}>
                      <SelectTrigger className='h-8 w-64 max-w-full' aria-label='Fator do eixo horizontal'>
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        {factorColumns.map(c => (
                          <SelectItem key={c} value={c}>
                            {c}
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                  </span>
                }
                chart={<ScatterPlot data={scatter} highlight={best.cenario} xLabel={shortName(factor, 40)} xFormat={value => nf(value, 2)} yFormat={value => usd(value, 0)} yAxisFormat={thousands} height={280} />}
                footer={
                  topEffect ? (
                    <p className='text-muted-foreground text-xs'>
                      O fator de maior efeito é <strong>{topEffect.name}</strong> (Spearman {signed(topEffect.value)}).
                    </p>
                  ) : null
                }
              />
            )}
          </TabsPanel>

          <TabsPanel value='scenarios'>
            <Card>
              <CardHeader>
                <CardTitle>Tabela de cenários</CardTitle>
                <CardDescription>
                  Cada linha é um cenário S<sub>i</sub>; <strong>Res</strong> é a margem sobre o custo de alimentação; o cenário ótimo está destacado.
                </CardDescription>
              </CardHeader>
              <CardContent>{scenarioTable}</CardContent>
            </Card>
          </TabsPanel>
        </div>
      </Tabs>
    </div>
  )
}
