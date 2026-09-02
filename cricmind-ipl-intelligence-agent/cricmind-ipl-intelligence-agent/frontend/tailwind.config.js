/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      colors: {
        cricmind: {
          primary: '#0B3D91',
          accent: '#FF6B00',
          dark: '#0A0F1E',
        },
      },
    },
  },
  plugins: [],
}
