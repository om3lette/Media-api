import { createApp } from "vue";
import { createPinia } from "pinia";
import "./styles.css";

import App from "./App.vue";

import PrimeVue from "primevue/config";
import Aura from "@primevue/themes/aura";
import "primeicons/primeicons.css";

import router from "./router/router";
import Tooltip from "primevue/tooltip";
import ToastService from "primevue/toastservice";
import { createI18n } from "vue-i18n";
import { defaultLocale, fallbackLocale, languages } from "./locales/locales";

export const app = createApp(App);
const pinia = createPinia();

const i18n = createI18n({
  legacy: false,
  locale: defaultLocale,
  fallbackLocale: fallbackLocale,
  messages: {
    ru: languages.ru,
    en: languages.en
  }
});

app.use(i18n);
app.use(pinia);
app.use(PrimeVue, {
  theme: {
    preset: Aura
  }
});

app.use(router);
app.use(ToastService);
app.directive("tooltip", Tooltip);
app.mount("#app");
