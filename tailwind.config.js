/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./templates/**/*.html",
    "./templates/**/*.js"
  ],
  safelist: [
    // Only safelist essential dynamic classes that might be generated at runtime
    'theme-light',
    'theme-classic',
    'theme-vibrant',
  ],
  theme: {
    extend: {
      fontFamily: {
        'gujarati': ['Noto Serif Gujarati', 'serif'],
      },
      colors: {
        // Light Theme - Modern and clean with blue accents
        light: {
          primary: '#2196F3',
          secondary: '#64B5F6',
          accent: '#FFC107',
          success: '#4CAF50',
          background: '#F5F7FA',
          text: '#1F2937',
          'text-secondary': '#6B7280',
        },
        // Classic Theme - Professional and timeless
        classic: {
          primary: '#1976D2',
          secondary: '#455A64',
          accent: '#FF9800',
          success: '#388E3C',
          background: '#FAFAFA',
          text: '#212121',
          'text-secondary': '#757575',
        },
        // Vibrant Theme - Bold and energetic
        vibrant: {
          primary: '#E91E63',
          secondary: '#9C27B0',
          accent: '#00BCD4',
          success: '#8BC34A',
          background: '#FFF3E0',
          text: '#1A1A1A',
          'text-secondary': '#616161',
        },
        // Legacy colors for backward compatibility
        primary: {
          50: '#E3F2FD',
          100: '#BBDEFB',
          500: '#2196F3',
          600: '#1E88E5',
          700: '#1976D2',
        },
        success: {
          50: '#E8F5E9',
          100: '#C8E6C9',
          500: '#4CAF50',
          600: '#43A047',
        }
      },
      spacing: {
        '18': '4.5rem',
        '22': '5.5rem',
        '26': '6.5rem',
        '30': '7.5rem',
        '128': '32rem',
        '144': '36rem',
      },
      boxShadow: {
        'colored': '0 10px 40px -10px rgba(33, 150, 243, 0.3)',
        'colored-lg': '0 20px 60px -15px rgba(33, 150, 243, 0.4)',
        'colored-xl': '0 25px 80px -20px rgba(33, 150, 243, 0.5)',
        'success': '0 10px 40px -10px rgba(76, 175, 80, 0.3)',
        'success-lg': '0 20px 60px -15px rgba(76, 175, 80, 0.4)',
        'vibrant': '0 10px 40px -10px rgba(233, 30, 99, 0.3)',
        'vibrant-lg': '0 20px 60px -15px rgba(233, 30, 99, 0.4)',
      },
      borderRadius: {
        '4xl': '2rem',
        '5xl': '2.5rem',
        '6xl': '3rem',
      },
      backgroundImage: {
        'gradient-radial': 'radial-gradient(var(--tw-gradient-stops))',
        'gradient-conic': 'conic-gradient(from 180deg at 50% 50%, var(--tw-gradient-stops))',
        'gradient-radial-at-t': 'radial-gradient(ellipse at top, var(--tw-gradient-stops))',
        'gradient-radial-at-b': 'radial-gradient(ellipse at bottom, var(--tw-gradient-stops))',
        'gradient-radial-at-l': 'radial-gradient(ellipse at left, var(--tw-gradient-stops))',
        'gradient-radial-at-r': 'radial-gradient(ellipse at right, var(--tw-gradient-stops))',
      },
      backdropBlur: {
        xs: '2px',
      },
    },
  },
  plugins: [],
}
