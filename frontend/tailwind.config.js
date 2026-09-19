/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      colors: {
        ink: {
          DEFAULT: "#12151B",
          panel: "#1A1F28",
          line: "#272E39",
        },
        parchment: {
          DEFAULT: "#ECE8DF",
          dim: "#9CA1AC",
        },
        signal: {
          DEFAULT: "#5FA8D3",
          dim: "#3E6E8C",
          bright: "#8FC4E3",
        },
        flag: "#C77B6C",
      },
      fontFamily: {
        serif: ["'Source Serif 4'", "Georgia", "serif"],
        sans: ["'Inter'", "system-ui", "sans-serif"],
      },
      boxShadow: {
        panel: "0 1px 0 rgba(255,255,255,0.03) inset, 0 20px 60px -30px rgba(0,0,0,0.6)",
      },
    },
  },
  plugins: [],
};
