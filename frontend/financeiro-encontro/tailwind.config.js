/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./src/**/*.{html,ts}'],
  corePlugins: {
    preflight: false, // Material handles base CSS resets
  },
  theme: {
    extend: {
      // Expõe os tokens M3 do Material como classes Tailwind
      // Ex: bg-primary, text-on-surface, border-outline
      colors: {
        primary:             'var(--mat-sys-primary)',
        'on-primary':        'var(--mat-sys-on-primary)',
        'primary-container': 'var(--mat-sys-primary-container)',
        'on-primary-container': 'var(--mat-sys-on-primary-container)',
        secondary:           'var(--mat-sys-secondary)',
        'on-secondary':      'var(--mat-sys-on-secondary)',
        tertiary:            'var(--mat-sys-tertiary)',
        'on-tertiary':       'var(--mat-sys-on-tertiary)',
        surface:             'var(--mat-sys-surface)',
        'on-surface':        'var(--mat-sys-on-surface)',
        'surface-variant':   'var(--mat-sys-surface-variant)',
        'on-surface-variant':'var(--mat-sys-on-surface-variant)',
        'surface-container': 'var(--mat-sys-surface-container)',
        'surface-container-low': 'var(--mat-sys-surface-container-low)',
        outline:             'var(--mat-sys-outline)',
        'outline-variant':   'var(--mat-sys-outline-variant)',
        error:               'var(--mat-sys-error)',
        'on-error':          'var(--mat-sys-on-error)',
        'error-container':   'var(--mat-sys-error-container)',
        'on-error-container':'var(--mat-sys-on-error-container)',
      },
    },
  },
  plugins: [],
};
