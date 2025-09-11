/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  safelist: [
    { pattern: /bg-(primary|secondary|accent|muted|foreground|background|border|black|titlebar)\/\d+/ },
    { pattern: /border-(primary|secondary|accent|muted|foreground|background|border)\/\d+/ },
    { pattern: /ring-(primary|secondary|accent|muted|foreground|background|border)\/\d+/ },
    { pattern: /bg-titlebar(-hover|-close-hover)?/ },
    { pattern: /text-titlebar(-foreground)?/ },
    'hover:bg-titlebar-hover',
    'hover:bg-titlebar-close-hover',
  ],
  darkMode: ['class'],
  theme: {
    extend: {
      colors: {
        border: "var(--border)",
        input: "var(--input)",
        ring: "var(--ring)",
        background: "var(--background)",
        foreground: "var(--foreground)",
        primary: {
          DEFAULT: "var(--primary)",
          foreground: "var(--primary-foreground)",
        },
        secondary: {
          DEFAULT: "var(--secondary)",
          foreground: "var(--secondary-foreground)",
        },
        destructive: {
          DEFAULT: "var(--destructive)",
          foreground: "var(--destructive-foreground)",
        },
        muted: {
          DEFAULT: "var(--muted)",
          foreground: "var(--muted-foreground)",
        },
        accent: {
          DEFAULT: "var(--accent)",
          foreground: "var(--accent-foreground)",
        },
        popover: {
          DEFAULT: "var(--popover)",
          foreground: "var(--popover-foreground)",
        },
        card: {
          DEFAULT: "var(--card)",
          foreground: "var(--card-foreground)",
        },
        // Title bar colors
        titlebar: {
          DEFAULT: "var(--titlebar)",
          foreground: "var(--titlebar-foreground)",
          hover: "var(--titlebar-hover)",
          'close-hover': "var(--titlebar-close-hover)",
        },
        // Gaming theme colors
        'cyber-neon': {
          50: '#f0f9ff',
          100: '#e0f2fe',
          200: '#bae6fd',
          300: '#7dd3fc',
          400: '#38bdf8',
          500: '#0ea5e9',
          600: '#0284c7',
          700: '#0369a1',
          800: '#075985',
          900: '#0c4a6e',
        },
        'dragon-gold': {
          50: '#fefce8',
          100: '#fef9c3',
          200: '#fef08a',
          300: '#fde047',
          400: '#facc15',
          500: '#eab308',
          600: '#ca8a04',
          700: '#a16207',
          800: '#854d0e',
          900: '#713f12',
        },
        'shadow-knight': {
          50: '#f8fafc',
          100: '#f1f5f9',
          200: '#e2e8f0',
          300: '#cbd5e1',
          400: '#94a3b8',
          500: '#64748b',
          600: '#475569',
          700: '#334155',
          800: '#1e293b',
          900: '#0f172a',
        },
      },
      borderRadius: {
        lg: "var(--radius)",
        md: "calc(var(--radius) - 2px)",
        sm: "calc(var(--radius) - 4px)",
      },
      keyframes: {
        "pulse-glow": {
          "0%, 100%": { 
            opacity: "0.2", 
            transform: "scale(1)" 
          },
          "50%": { 
            opacity: "0.4", 
            transform: "scale(1.05)" 
          },
        },
        "float": {
          "0%, 100%": { 
            transform: "translateY(0px) rotate(0deg)" 
          },
          "50%": { 
            transform: "translateY(-10px) rotate(180deg)" 
          },
        },
        "twinkle": {
          "0%, 100%": { 
            opacity: "0", 
            transform: "scale(0.5)" 
          },
          "50%": { 
            opacity: "1", 
            transform: "scale(1)" 
          },
        },
        "card-entrance": {
          "0%": { 
            opacity: "0", 
            transform: "translateY(20px) scale(0.95)" 
          },
          "100%": { 
            opacity: "1", 
            transform: "translateY(0) scale(1)" 
          },
        },
        "button-press": {
          "0%": { transform: "scale(1)" },
          "50%": { transform: "scale(0.98)" },
          "100%": { transform: "scale(1)" },
        },
        "slide-down": {
          "0%": { 
            opacity: "0", 
            transform: "translateY(-10px)" 
          },
          "100%": { 
            opacity: "1", 
            transform: "translateY(0)" 
          },
        },
      },
      animation: {
        "pulse-glow": "pulse-glow 8s ease-in-out infinite",
        "float": "float 12s ease-in-out infinite",
        "drift": "drift 15s ease-in-out infinite",
        "hover": "hover 10s ease-in-out infinite",
        "twinkle": "twinkle 6s ease-in-out infinite",
        "card-entrance": "card-entrance 0.6s ease-out",
        "button-press": "button-press 0.2s ease-in-out",
        "slide-down": "slide-down 0.3s ease-out",
      },
    },
  },
  plugins: [
    require('@tailwindcss/forms'),
  ],
}

