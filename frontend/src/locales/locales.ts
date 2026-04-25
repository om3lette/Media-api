import ru from "./ru.json";
import en from "./en.json";
import type { Locale } from "@/types/types";

export const languages = {
  ru,
  en
};

export const availableLocales: Locale[] = [
  { code: "ru", name: "Русский" },
  { code: "en", name: "English" }
];

export const defaultLocale: string = "ru";
export const fallbackLocale: string = "en";
export const localeStorageKey: string = "locale";
