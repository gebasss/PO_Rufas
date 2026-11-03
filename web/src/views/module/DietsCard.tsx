'use client'

import { useMemo, useState } from 'react'

import { PlusIcon, SearchIcon, Trash2Icon, WandSparklesIcon } from 'lucide-react'

import { feedTitle } from '@/components/FeedPicker'
import { NumberInput } from '@/components/shared'
import { Alert, AlertDescription } from '@/components/ui/alert'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { Table, TableBody, TableCell, TableFooter, TableHead, TableHeader, TableRow } from '@/components/ui/table'
import { nf } from '@/lib/format'
import type { Feed } from '@/lib/types'

import { MAX_DIETS, standardName, type ModuleState } from './model'

const MAX_SUGGESTIONS = 8

interface Props {
  state: ModuleState
  library: Record<number, Feed>
  feeds: Feed[] | null
  libraryError: string | null
  notice: string | null
  estimatedIntake: number | null
  onAddFeed: (id: number) => void
  onRemoveFeed: (id: number) => void
  onAmount: (uid: number, id: number, value: number) => void
  onName: (uid: number, name: string) => void
  onAddDiet: () => void
  onRemoveDiet: (uid: number) => void
  onExamples: () => void
}

function FeedAdder({ feeds, taken, onAdd }: { feeds: Feed[]; taken: number[]; onAdd: (id: number) => void }) {
  const [query, setQuery] = useState('')
  const suggestions = useMemo(() => {
    const q = query.trim().toLowerCase()

    if (!q) return []

    return feeds.filter(f => !taken.includes(f.id) && feedTitle(f).toLowerCase().includes(q))
  }, [feeds, taken, query])

  return (
    <div className='space-y-2'>
      <div className='relative max-w-md'>
        <SearchIcon className='text-muted-foreground pointer-events-none absolute top-1/2 left-2.5 size-4 -translate-y-1/2' />
        <Input
          type='search'
          value={query}
          onChange={e => setQuery(e.target.value)}
          placeholder='Adicionar alimento (soja, milho, silagem…)'
          className='pl-8'
          aria-label='Buscar alimento para adicionar à tabela'
        />
      </div>
      {query.trim() && (
        <div className='max-w-md rounded-lg border' role='listbox' aria-label='Alimentos encontrados'>
          {suggestions.slice(0, MAX_SUGGESTIONS).map(feed => (
            <button
              key={feed.id}
              type='button'
              role='option'
              aria-selected={false}
              className='hover:bg-muted/60 flex w-full flex-col items-start border-b px-2.5 py-2 text-left text-sm last:border-b-0'
              onClick={() => {
                onAdd(feed.id)
                setQuery('')
              }}
            >
              <span>{feedTitle(feed)}</span>
              <span className='text-muted-foreground text-xs'>
                {feed.kind} · PB {nf(feed.cp, 0)}% · FDN {nf(feed.ndf, 0)}%
              </span>
            </button>
          ))}
          {suggestions.length === 0 && <p className='text-muted-foreground p-3 text-sm'>Nenhum alimento encontrado.</p>}
          {suggestions.length > MAX_SUGGESTIONS && (
            <p className='text-muted-foreground p-2 text-center text-xs'>
              Mostrando {MAX_SUGGESTIONS} de {suggestions.length}. Refine a busca.
            </p>
          )}
        </div>
      )}
    </div>
  )
}

export default function DietsCard({
  state,
  library,
  feeds,
  libraryError,
  notice,
  estimatedIntake,
  onAddFeed,
  onRemoveFeed,
  onAmount,
  onName,
  onAddDiet,
  onRemoveDiet,
  onExamples
}: Props) {
  const empty = state.diets.length === 0
  const totals = state.diets.map(diet =>
    state.feedIds.reduce((sum, id) => sum + (Number.isFinite(diet.amounts[id]) ? Math.max(diet.amounts[id], 0) : 0), 0)
  )

  return (
    <Card>
      <CardHeader>
        <CardTitle>Dietas</CardTitle>
        <CardDescription>
          Dietas já montadas, em kg de matéria seca por dia, com alimentos da biblioteca do {standardName(state.standard)}. Até{' '}
          {MAX_DIETS} dietas por avaliação.
        </CardDescription>
      </CardHeader>
      <CardContent className='space-y-4'>
        {notice && (
          <Alert>
            <AlertDescription>{notice}</AlertDescription>
          </Alert>
        )}
        {libraryError && (
          <Alert variant='destructive'>
            <AlertDescription>{libraryError}</AlertDescription>
          </Alert>
        )}

        {empty ? (
          <div className='text-muted-foreground flex flex-col items-start gap-3 text-sm'>
            <p>Nenhuma dieta ainda. Adicione uma dieta e escolha os alimentos, ou comece por um exemplo.</p>
            <div className='flex flex-wrap gap-2'>
              <Button size='sm' onClick={onExamples} disabled={!feeds}>
                <WandSparklesIcon /> Carregar dietas de exemplo
              </Button>
              <Button size='sm' variant='outline' onClick={onAddDiet}>
                <PlusIcon /> Dieta
              </Button>
            </div>
          </div>
        ) : (
          <>
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead className='min-w-48'>Alimento</TableHead>
                  {state.diets.map(diet => (
                    <TableHead key={diet.uid} className='min-w-36'>
                      <div className='flex items-center gap-1'>
                        <Input
                          className='h-8 min-w-24'
                          value={diet.name}
                          aria-label='Nome da dieta'
                          onChange={e => onName(diet.uid, e.target.value)}
                        />
                        <Button
                          variant='ghost'
                          size='icon-sm'
                          aria-label={`Remover a dieta ${diet.name || 'sem nome'}`}
                          onClick={() => onRemoveDiet(diet.uid)}
                        >
                          <Trash2Icon />
                        </Button>
                      </div>
                    </TableHead>
                  ))}
                  <TableHead className='w-10' />
                </TableRow>
              </TableHeader>
              <TableBody>
                {state.feedIds.length === 0 && (
                  <TableRow>
                    <TableCell colSpan={state.diets.length + 2} className='text-muted-foreground'>
                      Adicione alimentos abaixo.
                    </TableCell>
                  </TableRow>
                )}
                {state.feedIds.map(id => {
                  const feed = library[id]
                  const title = feed ? feedTitle(feed) : `Alimento ${id}`

                  return (
                    <TableRow key={id}>
                      <TableCell>
                        <span className='block text-sm leading-snug'>{title}</span>
                        {feed && <span className='text-muted-foreground block text-xs'>{feed.kind}</span>}
                      </TableCell>
                      {state.diets.map(diet => (
                        <TableCell key={diet.uid}>
                          <NumberInput
                            step={0.1}
                            min={0}
                            value={diet.amounts[id] ?? 0}
                            onChange={value => onAmount(diet.uid, id, value)}
                            aria-label={`${title} na dieta ${diet.name || 'sem nome'}, em kg de matéria seca por dia`}
                          />
                        </TableCell>
                      ))}
                      <TableCell>
                        <Button
                          variant='ghost'
                          size='icon-sm'
                          aria-label={`Remover ${title} da tabela`}
                          onClick={() => onRemoveFeed(id)}
                        >
                          <Trash2Icon />
                        </Button>
                      </TableCell>
                    </TableRow>
                  )
                })}
              </TableBody>
              <TableFooter>
                <TableRow>
                  <TableCell>
                    Total (kg MS/dia)
                    {estimatedIntake !== null && (
                      <span className='text-muted-foreground block text-xs font-normal'>
                        consumo estimado: {nf(estimatedIntake, 1)}
                      </span>
                    )}
                  </TableCell>
                  {totals.map((total, i) => (
                    <TableCell key={state.diets[i].uid} className='text-right font-semibold tabular-nums'>
                      {nf(total, 2)}
                    </TableCell>
                  ))}
                  <TableCell />
                </TableRow>
              </TableFooter>
            </Table>

            <div className='flex flex-wrap gap-2'>
              <Button
                variant='outline'
                size='sm'
                onClick={onAddDiet}
                disabled={state.diets.length >= MAX_DIETS}
                title={state.diets.length >= MAX_DIETS ? `No máximo ${MAX_DIETS} dietas` : undefined}
              >
                <PlusIcon /> Dieta
              </Button>
              <Button variant='outline' size='sm' onClick={onExamples} disabled={!feeds}>
                <WandSparklesIcon /> Dietas de exemplo
              </Button>
            </div>
          </>
        )}

        {feeds && !empty && <FeedAdder feeds={feeds} taken={state.feedIds} onAdd={onAddFeed} />}
      </CardContent>
    </Card>
  )
}
