import type { Config } from 'tailwindcss'

export default {
  darkMode: 'class',
  content: [
    './components/**/*.{js,vue,ts}',
    './layouts/**/*.vue',
    './pages/**/*.vue',
    './app.vue',
  ],
  theme: {
    extend: {
      fontFamily: {
        roboto: ['Roboto', 'sans-serif']
      },
      safelist: [
        'bg-purple-500',
        'bg-blue-500',
        'bg-green-500',
        'bg-amber-500',
        'bg-rose-500',
        'bg-indigo-500',
        'bg-amber-50',
        'bg-amber-100',
        'text-amber-600',
        'text-amber-700',
        'bg-purple-50',
        'bg-purple-100',
        'text-purple-600',
        'text-purple-700',
        'bg-blue-50',
        'bg-blue-100',
        'text-blue-600',
        'text-blue-700',
        'bg-green-50',
        'bg-green-100',
        'text-green-600',
        'text-green-700',
        'bg-rose-50',
        'bg-rose-100',
        'text-rose-600',
        'text-rose-700',
        'bg-indigo-50',
        'bg-indigo-100',
        'text-indigo-600',
        'text-indigo-700'
      ],
      colors: {
        primary: {
          50: 'rgb(var(--color-primary-50) / <alpha-value>)',
          100: 'rgb(var(--color-primary-100) / <alpha-value>)',
          200: 'rgb(var(--color-primary-200) / <alpha-value>)',
          300: 'rgb(var(--color-primary-300) / <alpha-value>)',
          400: 'rgb(var(--color-primary-400) / <alpha-value>)',
          500: 'rgb(var(--color-primary-500) / <alpha-value>)',
          600: 'rgb(var(--color-primary-600) / <alpha-value>)',
          700: 'rgb(var(--color-primary-700) / <alpha-value>)',
          800: 'rgb(var(--color-primary-800) / <alpha-value>)',
          900: 'rgb(var(--color-primary-900) / <alpha-value>)',
          950: 'rgb(var(--color-primary-950) / <alpha-value>)',
        },

      },
      animation: {
        'bounce-slow': 'bounce 3s linear infinite',
      },
    },
  },
  plugins: [
    require('@tailwindcss/forms'),
  ],
} satisfies Config