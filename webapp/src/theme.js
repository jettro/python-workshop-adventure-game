import { createSystem, defaultConfig, defineConfig } from "@chakra-ui/react";

const config = defineConfig({
  globalCss: {
    body: {
      bg: "#0f1117",
      color: "#e2e8f0",
      fontFamily: "'Be Vietnam Pro', sans-serif",
    },
  },
  theme: {
    tokens: {
      colors: {
        brand: {
          50: { value: "#fef9e7" },
          100: { value: "#fceeb3" },
          200: { value: "#fae27f" },
          300: { value: "#f7d64b" },
          400: { value: "#f4c025" },
          500: { value: "#f4c025" },
          600: { value: "#c9991e" },
          700: { value: "#9e7317" },
          800: { value: "#734d10" },
          900: { value: "#482709" },
        },
      },
    },
  },
});

export const system = createSystem(defaultConfig, config);
