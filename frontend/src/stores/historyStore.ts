import { defineStore } from "pinia";
import { useStorage } from "@vueuse/core";
import type { RequestData } from "@/types/requests";
import { MAX_ENTRIES } from "@/constants/history";
import type { SyncPayload } from "@/types/api";
import { statusToReadable } from "@/utils";

export const useHistoryStore = defineStore("history", () => {
  const history = useStorage("history", [] as RequestData[]);
  const initialized = useStorage("history-initialized", new Set() as Set<string>);

  function addEntry(rid: string, operations: string[], filename: string) {
    history.value.push({
      id: rid,
      filename,
      timestamp: Date.now(),
      operations,
      status: "queued",
      currentStage: -1,
      totalStages: -1,
      stageProgress: 0,
      expired: false
    });
    if (history.value.length <= MAX_ENTRIES) return;
    history.value.slice(0, MAX_ENTRIES);
  }

  function getRequestById(rid: string): RequestData | undefined {
    return history.value.find((e) => e.id === rid);
  }

  function updateStatus(rid: string, newStatus: string, isExpired: boolean = false): boolean {
    const entry: RequestData | undefined = getRequestById(rid);

    if (!entry) {
      console.warn(`Unable to find request with id: ${rid}`);
      return false;
    }

    if (isExpired) {
      initialized.value.delete(rid);
    }

    entry.status = newStatus;
    entry.expired = isExpired;
    return true;
  }

  function isInitialized(rid: string) {
    return initialized.value.has(rid);
  }

  function updateStage(rid: string, newStage: number): boolean {
    const entry: RequestData | undefined = getRequestById(rid);
    if (!entry) return false;

    entry.currentStage = newStage;
    entry.stageProgress = 0;
    return true;
  }

  function updateProgress(rid: string, progress: number): boolean {
    const entry: RequestData | undefined = getRequestById(rid);
    if (!entry) return false;

    if (progress > 100 || progress < 0) {
      console.error(`Stage progress out of range: ${progress}`);
    }

    entry.stageProgress = Math.max(Math.min(progress, 100), 0);
    return true;
  }

  function syncRequestStatus(payload: SyncPayload): boolean {
    const requestEntry: RequestData | undefined = getRequestById(payload.rid);
    if (!requestEntry) {
      console.warn(`No history entry found for request: ${payload.rid}`);
      return false;
    }

    if (payload.status == 5) {
      updateStatus(payload.rid, "deleted", true);
      return true;
    }

    // TODO: Add checks for data validation?
    requestEntry.status = statusToReadable(payload.status);
    requestEntry.currentStage = payload.curStage as number;
    requestEntry.totalStages = payload.totalStages as number;
    requestEntry.stageProgress = payload.pct as number;

    if (!payload.totalStages || payload.totalStages <= 0) return true;

    initialized.value.add(payload.rid);
    if (initialized.value.size > MAX_ENTRIES) {
      for (const request of getRequestsInProgress()) {
        if (!initialized.value.has(request.id)) {
          initialized.value.delete(request.id);
        }
      }
    }
    return true;
  }

  function getRequestsInProgress(): RequestData[] {
    return history.value.filter(
      (data) => data.id && ["queued", "processing"].includes(data.status)
    );
  }

  function $reset(): void {
    history.value = [];
  }

  return {
    history,
    initialized,
    isInitialized,
    addEntry,
    getRequestsInProgress,
    syncRequestStatus,
    getRequestById,
    updateStatus,
    updateStage,
    updateProgress,
    $reset
  };
});
