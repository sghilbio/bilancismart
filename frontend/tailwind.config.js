/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          DEFAULT: '#1B365D', // Navy blue for reliability
          light: '#2C4B7C',
          dark: '#0F2440'
        },
        secondary: {
          DEFAULT: '#7C9070', // Sage green for growth
          light: '#94A889',
          dark: '#647857'
        },
        success: '#4CAF50',
        warning: '#FFC107',
        error: '#F44336',
        background: '#F5F7FA',
        surface: '#FFFFFF',
        text: {
          primary: '#1A1A1A',
          secondary: '#666666',
          disabled: '#9E9E9E'
        }
      },
    },
  },
  plugins: [],
} 