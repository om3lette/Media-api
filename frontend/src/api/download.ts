import { UrlType } from "@/types/api";
import { getUrl } from "./urlProvider";

import.meta.env.BASE_URL;

export const getRequestOutput = async (requestId: string) => {
  return await fetch(new URL(`download/${requestId}/`, getUrl(UrlType.API)));
};
