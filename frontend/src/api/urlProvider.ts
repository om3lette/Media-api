import { UrlType } from "@/types/api";

const env = import.meta.env;

export const getBaseUrl = () => {
  return env.VITE_BASE_URL ?? window.location.origin;
};

export const getUrl = (type: UrlType) => {
  const baseUrl: string = getBaseUrl();
  let fullUrl, subpath, protocol;
  switch (type) {
    case UrlType.API:
      fullUrl = env.VITE_API_BASE_URL;
      subpath = "api/v1/";
      break;
    case UrlType.WS_STATUS:
      fullUrl = env.VITE_API_BASE_URL;
      subpath = "api/v1/status/ws/";
      if (location.protocol === "https:") {
        protocol = "wss";
      } else {
        protocol = "ws";
      }
      break;
    default:
      throw new Error(`Unknown url type: ${type}`);
  }

  let result;
  if (fullUrl != null) {
    result = new URL(fullUrl);
  } else {
    result = new URL(subpath, baseUrl);
  }

  if (protocol) result.protocol = protocol;
  return result;
};
