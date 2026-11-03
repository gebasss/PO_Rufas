'use client'

import { RotateCcwIcon } from 'lucide-react'

import { Segmented } from '@/components/Segmented'
import { NumberInput } from '@/components/shared'
import { Alert, AlertDescription } from '@/components/ui/alert'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Label } from '@/components/ui/label'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { Skeleton } from '@/components/ui/skeleton'
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table'
import { nf } from '@/lib/format'
import type { ModuleCategory, ModuleDefaults, ModuleField, ModuleRequirements, NutrientStandard } from '@/lib/types'

import { ANIMAL_TYPES, CATEGORIES, HOUSING_LABELS, STANDARDS, standardName, type ModuleState } from './model'

interface Props {
  state: ModuleState
  defaults: ModuleDefaults | null
  defaultsError: string | null
  requirements: ModuleRequirements | null
  requirementsLoading: boolean
  requirementsError: string | null
  problems: string[]
  onStandard: (value: NutrientStandard) => void
  onCategory: (value: ModuleCategory) => void
  onAnimalType: (value: string) => void
  onCow: (key: string, value: number | string) => void
  onOverride: (key: string, value: number | undefined) => void
}

function FieldInput({
  field,
  value,
  onChange,
  hint
}: {
  field: ModuleField
  value: number | string | undefined
  onChange: (value: number | string) => void
  hint?: string
}) {
  const id = `cow-${field.key}`
  const label = `${field.label}${field.unit ? ` (${field.unit})` : ''}`

  return (
    <div className='flex flex-col justify-end gap-1.5'>
      <Label htmlFor={id} className='leading-snug'>
        {label}
        {field.required ? <span className='text-destructive' aria-label='obrigatório'> *</span> : null}
      </Label>
      {field.choices.length ? (
        <Select
          value={typeof value === 'string' ? value : field.choices[0]}
          items={field.choices.map(choice => ({ value: choice, label: HOUSING_LABELS[choice] ?? choice }))}
          onValueChange={next => next && onChange(next)}
        >
          <SelectTrigger id={id} className='w-full'>
            <SelectValue />
          </SelectTrigger>
          <SelectContent>
            {field.choices.map(choice => (
              <SelectItem key={choice} value={choice}>
                {HOUSING_LABELS[choice] ?? choice}
              </SelectItem>
            ))}
          </SelectContent>
        </Select>
      ) : (
        <NumberInput
          className='h-9'
          step={field.integer ? 1 : 0.1}
          min={field.min ?? undefined}
          value={typeof value === 'number' ? value : Number.NaN}
          placeholder={hint}
          onChange={onChange}
          aria-label={label}
          id={id}
        />
      )}
    </div>
  )
}

export default function CowCard({
  state,
  defaults,
  defaultsError,
  requirements,
  requirementsLoading,
  requirementsError,
  problems,
  onStandard,
  onCategory,
  onAnimalType,
  onCow,
  onOverride
}: Props) {
  const fields = defaults?.fields ?? []
  const groups = {
    vaca: fields.filter(f => f.group === 'vaca'),
    lote: fields.filter(f => f.group === 'lote'),
    dieta: fields.filter(f => f.group === 'dieta')
  }
  const animalTypes = ANIMAL_TYPES[state.category]
  const rows = (defaults?.requirement_fields ?? []).filter(
    row => requirements?.calculated[row.key] != null || state.override[row.key] !== undefined
  )

  return (
    <Card>
      <CardHeader>
        <CardTitle>Vaca</CardTitle>
        <CardDescription>
          Padrão nutricional, categoria e características do animal. Os valores iniciais são um exemplo: troque-os pelos da
          vaca real.
        </CardDescription>
      </CardHeader>
      <CardContent className='space-y-6'>
        <div className='flex flex-wrap items-end gap-x-6 gap-y-4'>
          <div className='space-y-1.5'>
            <Label>Padrão nutricional</Label>
            <div>
              <Segmented
                label='Padrão nutricional'
                value={state.standard}
                options={STANDARDS}
                onChange={onStandard}
              />
            </div>
          </div>
          <div className='min-w-56 space-y-1.5'>
            <Label>Categoria</Label>
            <Select
              value={state.category}
              items={CATEGORIES}
              onValueChange={value => value && onCategory(value as ModuleCategory)}
            >
              <SelectTrigger className='w-full'>
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                {CATEGORIES.map(item => (
                  <SelectItem key={item.value} value={item.value}>
                    {item.label}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>
          {animalTypes.length > 1 && (
            <div className='min-w-44 space-y-1.5'>
              <Label>Tipo de animal</Label>
              <Select value={state.animalType} items={animalTypes} onValueChange={value => value && onAnimalType(value)}>
                <SelectTrigger className='w-full'>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  {animalTypes.map(item => (
                    <SelectItem key={item.value} value={item.value}>
                      {item.label}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
          )}
        </div>

        {defaultsError ? (
          <Alert variant='destructive'>
            <AlertDescription>{defaultsError}</AlertDescription>
          </Alert>
        ) : !defaults ? (
          <Skeleton className='h-40 w-full' />
        ) : (
          <>
            <div className='grid gap-4 sm:grid-cols-2 lg:grid-cols-4'>
              {groups.vaca.map(field => (
                <FieldInput key={field.key} field={field} value={state.cow[field.key]} onChange={v => onCow(field.key, v)} />
              ))}
            </div>

            {groups.lote.length > 0 && (
              <div className='space-y-2'>
                <h3 className='text-muted-foreground text-xs font-medium tracking-wider uppercase'>Lote (energia do NASEM)</h3>
                <p className='text-muted-foreground text-xs'>
                  O NASEM desconta da energia o metano e o nitrogênio urinário. Esses valores vêm do lote simulado pelo RuFaS e
                  não existem para uma vaca isolada. Sem eles, a restrição de energia fica “indisponível” e a dieta é marcada
                  como incompleta.
                </p>
                <div className='grid gap-4 sm:grid-cols-2 lg:grid-cols-4'>
                  {groups.lote.map(field => (
                    <FieldInput key={field.key} field={field} value={state.cow[field.key]} onChange={v => onCow(field.key, v)} />
                  ))}
                </div>
              </div>
            )}

            {groups.dieta.length > 0 && (
              <div className='space-y-2'>
                <h3 className='text-muted-foreground text-xs font-medium tracking-wider uppercase'>
                  Ração anterior (opcional)
                </h3>
                <p className='text-muted-foreground text-xs'>
                  Vazio = o valor vem da própria dieta avaliada, como o RuFaS faz com a ração do dia anterior. Se preencher,
                  o valor vale para todas as dietas.
                </p>
                <div className='grid gap-4 sm:grid-cols-2 lg:grid-cols-4'>
                  {groups.dieta.map(field => (
                    <FieldInput
                      key={field.key}
                      field={field}
                      value={state.cow[field.key]}
                      hint='da dieta'
                      onChange={v => onCow(field.key, v)}
                    />
                  ))}
                </div>
              </div>
            )}

            {problems.length > 0 && (
              <Alert>
                <AlertDescription>
                  <ul className='list-disc space-y-0.5 pl-4'>
                    {problems.map(problem => (
                      <li key={problem}>{problem}</li>
                    ))}
                  </ul>
                </AlertDescription>
              </Alert>
            )}

            <div className='space-y-2'>
              <h3 className='text-muted-foreground text-xs font-medium tracking-wider uppercase'>Exigências</h3>
              <p className='text-muted-foreground text-xs'>
                Calculadas pelo RuFaS ({standardName(state.standard)}) com os padrões do RuFaS para a ração
                anterior. Na avaliação elas são recalculadas para cada dieta. Preencha “Sobrescrever” para usar o seu valor.
              </p>
              {requirementsError ? (
                <Alert variant='destructive'>
                  <AlertDescription>{requirementsError}</AlertDescription>
                </Alert>
              ) : problems.length > 0 ? (
                <p className='text-muted-foreground text-sm'>Complete os campos da vaca para ver as exigências.</p>
              ) : !requirements ? (
                <Skeleton className='h-32 w-full' />
              ) : (
                <div className={requirementsLoading ? 'opacity-60 transition-opacity' : 'transition-opacity'}>
                  <Table>
                    <TableHeader>
                      <TableRow>
                        <TableHead>Exigência</TableHead>
                        <TableHead className='text-right'>Calculada</TableHead>
                        <TableHead>Unidade</TableHead>
                        <TableHead className='w-44 text-right'>Sobrescrever</TableHead>
                        <TableHead className='w-10' />
                      </TableRow>
                    </TableHeader>
                    <TableBody>
                      {rows.map(row => {
                        const overridden = state.override[row.key] !== undefined

                        return (
                          <TableRow key={row.key}>
                            <TableCell>{row.label}</TableCell>
                            <TableCell className='text-right tabular-nums'>
                              {nf(requirements.calculated[row.key], 2)}
                            </TableCell>
                            <TableCell className='text-muted-foreground text-xs'>{row.unit}</TableCell>
                            <TableCell>
                              <NumberInput
                                value={state.override[row.key] ?? Number.NaN}
                                min={0}
                                step={0.1}
                                onChange={v => onOverride(row.key, Number.isFinite(v) ? v : undefined)}
                                aria-label={`Sobrescrever ${row.label}, em ${row.unit}`}
                                placeholder='calculada'
                              />
                            </TableCell>
                            <TableCell>
                              {overridden && (
                                <Button
                                  variant='ghost'
                                  size='icon-sm'
                                  aria-label={`Voltar ao valor calculado de ${row.label}`}
                                  onClick={() => onOverride(row.key, undefined)}
                                >
                                  <RotateCcwIcon />
                                </Button>
                              )}
                            </TableCell>
                          </TableRow>
                        )
                      })}
                    </TableBody>
                  </Table>
                  {requirements.warnings.length > 0 && (
                    <ul className='text-muted-foreground mt-2 list-disc space-y-0.5 pl-4 text-xs'>
                      {requirements.warnings.map(warning => (
                        <li key={warning}>{warning}</li>
                      ))}
                    </ul>
                  )}
                </div>
              )}
            </div>
          </>
        )}
      </CardContent>
    </Card>
  )
}
