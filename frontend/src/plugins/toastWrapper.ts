import { app } from "@/main";
import type { Severity } from "@/types/types.ts";

export default class toastWrapper {
  static defaultMessageLife = 3500;
  static defaultClosable = false;
  static defaultSeverity: Severity = "info";

  static infoSummarySelector = "toast-default.summary.info";
  static warnSummarySelector = "toast-default.summary.warn";
  static successSummarySelector = "toast-default.summary.success";
  static errorSummarySelector = "toast-default.summary.error";

  static addMessage(
    message: string,
    summary: string,
    severity: Severity = toastWrapper.defaultSeverity,
    life = toastWrapper.defaultMessageLife,
    closable = toastWrapper.defaultClosable
  ) {
    const toast = app.config.globalProperties.$toast;

    toast.add({
      summary,
      detail: message,
      life,
      closable,
      severity
    });
  }

  static info(
    message: string,
    summary?: string,
    life = toastWrapper.defaultMessageLife,
    closable = toastWrapper.defaultClosable
  ) {
    const t = app.config.globalProperties.$t;
    toastWrapper.addMessage(
      message,
      summary ?? t(toastWrapper.infoSummarySelector),
      "info",
      life,
      closable
    );
  }

  static success(
    message: string,
    summary?: string,
    life = toastWrapper.defaultMessageLife,
    closable = toastWrapper.defaultClosable
  ) {
    const t = app.config.globalProperties.$t;
    toastWrapper.addMessage(
      message,
      summary ?? t(toastWrapper.successSummarySelector),
      "success",
      life,
      closable
    );
  }

  static warn(
    message: string,
    summary?: string,
    life = toastWrapper.defaultMessageLife,
    closable = toastWrapper.defaultClosable
  ) {
    const t = app.config.globalProperties.$t;
    toastWrapper.addMessage(
      message,
      summary ?? t(toastWrapper.warnSummarySelector),
      "warn",
      life,
      closable
    );
  }

  static error(
    message: string,
    summary?: string,
    life = toastWrapper.defaultMessageLife,
    closable = toastWrapper.defaultClosable
  ) {
    const t = app.config.globalProperties.$t;
    toastWrapper.addMessage(
      message,
      summary ?? t(toastWrapper.errorSummarySelector),
      "error",
      life,
      closable
    );
  }
}
