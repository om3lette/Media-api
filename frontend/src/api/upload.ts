import { UrlType } from "@/types/api";
import { getUrl } from "./urlProvider";

export const postNewRequest = async (data: FormData) => {
  return await fetch(new URL("custom/", getUrl(UrlType.API)), {
    method: "Post",
    body: data
  });
};
