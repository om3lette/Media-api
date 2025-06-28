import type { Operations } from "./types";

export type RequestParams = {
  headers?: Record<string, string>;
  data?: object;
  isForm?: boolean;
  method: "Get" | "Post" | "Patch" | "Put" | "Delete";
  path: string;
};

export type Verdict = {
  ok: boolean;
  data: { [key: string]: any } | null;
  error: { type: string; data: string } | null;
};

export interface RequestData {
  id: string;
  filename: string;
  operations: Operations;
  timestamp: number;
  status: string;
  currentStage: number;
  totalStages: number;
  stageProgress: number;
  expired: boolean;
}
