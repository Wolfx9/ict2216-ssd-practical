import js from "@eslint/js";
import globals from "globals";
import pluginSecurity from "eslint-plugin-security";
import pluginNoUnsanitized from "eslint-plugin-no-unsanitized";

export default [
  {
    files: ["webapp/static/**/*.js"],
    languageOptions: {
      ecmaVersion: "latest",
      sourceType: "script",
      globals: {
        ...globals.browser,
      },
    },
    plugins: {
      security: pluginSecurity,
      "no-unsanitized": pluginNoUnsanitized,
    },
    rules: {
      ...js.configs.recommended.rules,
      ...pluginSecurity.configs.recommended.rules,
      ...pluginNoUnsanitized.configs.recommended.rules,
    },
  },
];
