'use client'

import { feedTitle } from '@/components/FeedPicker'
import PriceImport from '@/components/PriceImport'
import { NumberInput } from '@/components/shared'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table'
import type { Feed } from '@/lib/types'

import type { ModuleState } from './model'

interface Props {
  state: ModuleState
  library: Record<number, Feed>
  onSetting: (id: number, field: 'price' | 'min' | 'max', value: number) => void
  onPrices: (prices: Record<number, number>) => void
}

export default function PricesCard({ state, library, onSetting, onPrices }: Props) {
  return (
    <Card>
      <CardHeader>
        <CardTitle>Preços e limites</CardTitle>
        <CardDescription>
          Preço em dólares por kg de matéria seca (a conversão do CEPEA, de reais e de matéria natural fica para depois). Os
          valores iniciais são ilustrativos. Os limites por alimento (kg de MS por dia) entram como restrições da avaliação.
        </CardDescription>
      </CardHeader>
      <CardContent className='space-y-4'>
        <PriceImport standard={state.standard} selectedIds={state.feedIds} onApply={onPrices} />
        {state.feedIds.length === 0 ? (
          <p className='text-muted-foreground text-sm'>Os alimentos das dietas aparecem aqui.</p>
        ) : (
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead className='min-w-48'>Alimento</TableHead>
                <TableHead className='w-36 text-right'>Preço (US$/kg MS)</TableHead>
                <TableHead className='w-32 text-right'>Mínimo (kg/dia)</TableHead>
                <TableHead className='w-32 text-right'>Máximo (kg/dia)</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {state.feedIds.map(id => {
                const feed = library[id]
                const title = feed ? feedTitle(feed) : `Alimento ${id}`
                const setting = state.feedSettings[id]

                if (!setting) return null

                return (
                  <TableRow key={id}>
                    <TableCell className='text-sm leading-snug'>{title}</TableCell>
                    <TableCell>
                      <NumberInput
                        min={0}
                        value={setting.price}
                        onChange={v => onSetting(id, 'price', v)}
                        aria-label={`Preço de ${title}, em dólares por kg de matéria seca`}
                      />
                    </TableCell>
                    <TableCell>
                      <NumberInput
                        min={0}
                        step={0.1}
                        value={setting.min}
                        onChange={v => onSetting(id, 'min', v)}
                        aria-label={`Mínimo de ${title}, em kg de matéria seca por dia`}
                      />
                    </TableCell>
                    <TableCell>
                      <NumberInput
                        min={0}
                        step={0.1}
                        value={setting.max}
                        onChange={v => onSetting(id, 'max', v)}
                        aria-label={`Máximo de ${title}, em kg de matéria seca por dia`}
                      />
                    </TableCell>
                  </TableRow>
                )
              })}
            </TableBody>
          </Table>
        )}
      </CardContent>
    </Card>
  )
}
