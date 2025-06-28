import { UrlType } from "@/types/api";
import { getUrl } from "./urlProvider";

import.meta.env.BASE_URL;

export const getRequestStatus = async (requestId: string) => {
  return await fetch(new URL(`status/?request_id=${requestId}`, getUrl(UrlType.API)));
};

export const getSubPayload = (rid: string) => {
  return JSON.stringify({
    type: "sub",
    rid: rid
  });
};

export const getUnSubPayload = (rid: string) => {
  return JSON.stringify({
    type: "unsub",
    rid: rid
  });
};

export const getSyncPayload = (rid: string) => {
  return JSON.stringify({
    type: "sync",
    rid: rid
  });
};
