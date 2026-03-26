/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        aranet: {
          ink: "#1d1d1d",
          muted: "#5c5c5c",
          faint: "#9e9e9e",
          border: "#e0e0e0",
          surface: "#f5f5f5",
          page: "#fafafa",
          white: "#ffffff",
          red: "#e31e24",
          "red-hover": "#c91a1f",
          /** Aranet --v-theme-brandGreen: 23, 171, 31 */
          green: "#17ab1f",
        },
      },
      fontFamily: {
        sans: [
          '"Archivo"',
          "ui-sans-serif",
          "system-ui",
          "sans-serif",
        ],
        mono: ['"Source Code Pro"', "ui-monospace", "monospace"],
      },
      boxShadow: {
        aranet: "0 0 10px rgba(29, 29, 29, 0.1)",
      },
    },
  },
  plugins: [],
}
