import { operationIcons } from "./constants/icons";
import type { Operation } from "./types/types";
import { GB, MB, KB } from "./constants/file";

// Thanks: https://stackoverflow.com/a/49849482/20957519
export function isValidURL(url: string) {
  var res = url.match(
    /(http(s)?:\/\/.)?(www\.)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)/g
  );
  return res !== null;
}

export const getIconByOperation = (operation: Operation): string => {
  return operationIcons[operation] ?? "question";
};

export const timestampToReadable = (timestamp: number): string => {
  return new Intl.DateTimeFormat("ru-RU", {
    dateStyle: "short",
    timeStyle: "medium"
  }).format(timestamp);
};

const roundByTwo = (num: number) => {
  return Math.round(num * 100) / 100;
};

export const fileSizeToString = (fileSize: number) => {
  if (fileSize < MB) {
    return `${roundByTwo(fileSize / KB)} KB`;
  }
  if (fileSize < GB) {
    return `${roundByTwo(fileSize / MB)} MB`;
  }
  return `${roundByTwo(fileSize / GB)} GB`;
};

export const statusToReadable = (status: number): string => {
  switch (status) {
    case 0:
      return "queued";
    case 1:
      return "processing";
    case 2:
    case 3:
      return "completed";
    case 4:
      return "canceled";
    case 5:
      return "deleted";
    default:
      throw RangeError("Status out of range");
  }
};
