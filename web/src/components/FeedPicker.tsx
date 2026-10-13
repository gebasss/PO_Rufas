'use client'

import { useMemo, useState } from 'react'

import { SearchIcon, XIcon } from 'lucide-react'

import { NumberInput } from '@/components/shared'
import { Button } from '@/components/ui/button'
import { Checkbox } from '@/components/ui/checkbox'
import { Input } from '@/components/ui/input'
import { nf } from '@/lib/format'
import type { Feed } from '@/lib/types'
import { PRESET_BASE, PRESET_WIDE, useApp } from '@/providers/AppProvider'

export const feedTitle = (feed: Feed) =>
  feed.description && feed.description.toLowerCase() !== 'no' ? `${feed.name} — ${feed.description}` : feed.name

const MAX_RESULTS = 60

export default function FeedPicker() {
  const { feeds, feedById, selected, toggleFeed, setFeedField, applyPreset } = useApp()
  const [query, setQuery] = useState('')

  const results = useMemo(() => {
    const q = query.trim().toLowerCase()

    return feeds.filter(f => !q || feedTitle(f).toLowerCase().includes(q) || f.kind.toLowerCase().includes(q))
  }, [feeds, query])

  const selectedIds = Object.keys(selected).map(Number)

  return (
    <div className='space-y-4'>
      <div className='flex flex-wrap gap-2'>
        <Button variant='outline' size='sm' onClick={() => applyPreset(PRESET_BASE)}>
          Conjunto base
        </Button>
        <Button variant='outline' size='sm' onClick={() => applyPreset(PRESET_WIDE)}>
          Lista ampla
        </Button>
      </div>

      <div className='relative'>
        <SearchIcon className='text-muted-foreground pointer-events-none absolute top-1/2 left-2.5 size-4 -translate-y-1/2' />
        <Input
          type='search'
          value={query}
          onChange={e => setQuery(e.target.value)}
          placeholder='Buscar alimento (soja, arroz, milho…)'
          className='pl-8'
          aria-label='Buscar alimento'
        />
      </div>

      <div className='max-h-60 overflow-y-auto rounded-lg border' role='listbox' aria-label='Alimentos da NRC 2001'>
        {results.slice(0, MAX_RESULTS).map(feed => (
          <label
            key={feed.id}
            className='hover:bg-muted/60 flex cursor-pointer items-start gap-2.5 border-b px-2.5 py-2 text-sm last:border-b-0'
          >
            <Checkbox className='mt-0.5' checked={!!selected[feed.id]} onCheckedChange={() => toggleFeed(feed.id)} />
            <span className='min-w-0 flex-1'>
              <span className='block truncate'>{feedTitle(feed)}</span>
              <span className='text-muted-foreground block text-xs'>
                {feed.kind} · PB {nf(feed.cp, 0)}% · FDN {nf(feed.ndf, 0)}% · NEL {nf(feed.nel, 2)} Mcal/kg
              </span>
            </span>
          </label>
        ))}
        {results.length === 0 && <p className='text-muted-foreground p-3 text-sm'>Nenhum alimento encontrado.</p>}
        {results.length > MAX_RESULTS && (
          <p className='text-muted-foreground p-2 text-center text-xs'>
            Mostrando {MAX_RESULTS} de {results.length}. Refine a busca.
          </p>
        )}
      </div>

      <div className='space-y-2'>
        <h3 className='text-muted-foreground text-xs font-medium tracking-wider uppercase'>
          Selecionados ({selectedIds.length})
        </h3>
        {selectedIds.length === 0 ? (
          <p className='text-muted-foreground text-sm'>Nenhum alimento selecionado.</p>
        ) : (
          <div className='space-y-2'>
            {selectedIds.map(id => {
              const feed = feedById[id]
              const s = selected[id]
              const title = feed ? feedTitle(feed) : String(id)

              return (
                <div key={id} className='bg-muted/30 space-y-2 rounded-lg border p-2.5'>
                  <div className='flex items-start justify-between gap-2'>
                    <span className='text-xs leading-snug font-medium'>{title}</span>
                    <Button
                      variant='ghost'
                      size='icon-xs'
                      className='-mt-0.5 -mr-1 shrink-0'
                      aria-label={`Remover ${title}`}
                      onClick={() => toggleFeed(id)}
                    >
                      <XIcon />
                    </Button>
                  </div>
                  <div className='grid grid-cols-3 gap-2'>
                    <label className='space-y-1'>
                      <span className='text-muted-foreground block text-[11px]'>US$/kg MS</span>
                      <NumberInput
                        className='h-7 px-1.5 text-xs'
                        value={s.price}
                        onChange={v => setFeedField(id, 'price', v)}
                        aria-label={`Preço de ${title}, em dólares por kg de matéria seca`}
                      />
                    </label>
                    <label className='space-y-1'>
                      <span className='text-muted-foreground block text-[11px]'>mín. kg/dia</span>
                      <NumberInput
                        className='h-7 px-1.5 text-xs'
                        step={0.1}
                        min={0}
                        value={s.min}
                        onChange={v => setFeedField(id, 'min', v)}
                        aria-label={`Mínimo de ${title}, em kg de matéria seca por vaca por dia`}
                      />
                    </label>
                    <label className='space-y-1'>
                      <span className='text-muted-foreground block text-[11px]'>máx. kg/dia</span>
                      <NumberInput
                        className='h-7 px-1.5 text-xs'
                        step={0.1}
                        min={0}
                        value={s.max}
                        onChange={v => setFeedField(id, 'max', v)}
                        aria-label={`Máximo de ${title}, em kg de matéria seca por vaca por dia`}
                      />
                    </label>
                  </div>
                </div>
              )
            })}
          </div>
        )}
      </div>
    </div>
  )
}
