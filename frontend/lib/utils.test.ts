import { describe, it, expect } from 'vitest'
import { cn } from './utils'

describe('cn utility', () => {
  it('should merge tailwind classes correctly', () => {
    // Basic test
    expect(cn('text-red-500', 'bg-blue-500')).toBe('text-red-500 bg-blue-500')

    // Tailwind merge test: later class should override the earlier one
    expect(cn('p-4', 'p-8')).toBe('p-8')
    expect(cn('bg-red-500', 'bg-blue-500')).toBe('bg-blue-500')

    // Testing objects (clsx functionality)
    expect(cn('p-4', { 'bg-red-500': true, 'bg-blue-500': false })).toBe('p-4 bg-red-500')
    expect(cn('p-4', { 'text-white': true }, 'bg-black')).toBe('p-4 text-white bg-black')

    // Testing arrays (clsx functionality)
    expect(cn(['p-4', 'bg-red-500'], 'text-white')).toBe('p-4 bg-red-500 text-white')
    expect(cn(['p-4', ['bg-red-500', 'text-white']])).toBe('p-4 bg-red-500 text-white')

    // Falsy values test (clsx functionality)
    expect(cn('p-4', null, undefined, false, '', 'bg-red-500')).toBe('p-4 bg-red-500')
    expect(cn('p-4', false && 'bg-blue-500', 'bg-red-500')).toBe('p-4 bg-red-500')
  })

  it('handles arbitrary values and complex Tailwind merges', () => {
    // Margins with arbitrary values
    expect(cn('m-[2px]', 'm-[4px]')).toBe('m-[4px]')

    // Complex conditional and merge combinations
    expect(
      cn(
        'text-base font-bold',
        true && 'text-lg',
        { 'text-xl': false },
        'hover:text-red-500',
        'hover:text-blue-500'
      )
    ).toBe('font-bold text-lg hover:text-blue-500')
  })
})
