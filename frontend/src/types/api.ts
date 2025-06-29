export enum UrlType {
  API = 0,
  WS_STATUS = 1
}

export interface SyncPayload {
  rid: string;
  status: number;
  elapsedTime?: number;
  curStage?: number;
  totalStages?: number;
  pct?: number;
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

export enum ErrorCode {
  REQUEST_NOT_FOUND = 1,
  SUB_NOT_ACCEPTED,
  ALREADY_SUBSCRIBED,
  NOT_SUBSCRIBED
}

export interface ErrorPayload {
  rid: string;
  isMissing?: boolean;
  isValidation?: boolean;
  code: ErrorCode;
}
