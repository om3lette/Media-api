export enum UrlType {
  API = 0,
  WS_STATUS = 1
}

export interface SyncPayload {
  rid: string;
  status: number;
  elapsedTime: number;
  curStage: number;
  totalStages: number;
  pct: number;
}

export interface StatusPayload {
  rid: string;
  status: number;
}

export interface ProgressPayload {
  rid: string;
  pct: number;
}

export interface StagePayload {
  rid: string;
  curStage: number;
}

export interface ErrorPayload {
  rid: string;
  invalidId: boolean;
  detail: string;
}
