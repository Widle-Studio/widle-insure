import { cn } from './utils'

describe('cn utility', () => {
  it('should merge basic tailwind classes correctly', () => {
    expect(cn('text-red-500', 'bg-blue-500')).toBe('text-red-500 bg-blue-500')
  })

  it('should handle tailwind merge correctly: later class should override the earlier one', () => {
    expect(cn('p-4', 'p-8')).toBe('p-8')
    expect(cn('bg-red-500', 'bg-blue-500')).toBe('bg-blue-500')
  })

  it('should handle objects (clsx functionality)', () => {
    expect(cn('p-4', { 'bg-red-500': true, 'bg-blue-500': false })).toBe('p-4 bg-red-500')
    expect(cn('p-4', { 'text-white': true }, 'bg-black')).toBe('p-4 text-white bg-black')
  })

  it('should handle arrays (clsx functionality)', () => {
    expect(cn(['p-4', 'bg-red-500'], 'text-white')).toBe('p-4 bg-red-500 text-white')
    expect(cn(['p-4', ['bg-red-500', 'text-white']])).toBe('p-4 bg-red-500 text-white')
  })

  it('should handle falsy values (clsx functionality)', () => {
    expect(cn('p-4', null, undefined, false, '', 'bg-red-500')).toBe('p-4 bg-red-500')
    expect(cn('p-4', false && 'bg-blue-500', 'bg-red-500')).toBe('p-4 bg-red-500')
  })

  it('handles arbitrary values and complex Tailwind merges', () => {
    expect(cn('m-[2px]', 'm-[4px]')).toBe('m-[4px]')
  })

  it('handles complex conditional and merge combinations', () => {
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
