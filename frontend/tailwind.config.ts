/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx,vue}"],
  theme: {
    extend: {},
    screens: {
      "h-xs": { raw: "(min-height: 400px)" },
      "h-sm": { raw: "(min-height: 600px)" },
      "h-md": { raw: "(min-height: 720px)" },
      "h-lg": { raw: "(min-height: 1080px)" },
      "h-xl": { raw: "(min-height: 1440px)" },
      "h-2xl": { raw: "(min-height: 2160px)" }
    }
  },
  plugins: []
};
