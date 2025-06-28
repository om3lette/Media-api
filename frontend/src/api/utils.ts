export const getResponseStatus = async (url: string) => {
  const response = await fetch(url, {
    method: "HEAD"
  });
  return response.status;
};
