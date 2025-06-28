export const useNotification = () => {
  const requestPermission = async (): Promise<NotificationPermission | null> => {
    if (!("Notification" in window)) return new Promise(() => null);
    if (Notification.permission == "default") return await Notification.requestPermission();

    return Notification.permission;
  };

  const newNotification = async (title: string, options: Record<string, string> = {}) => {
    const permission: NotificationPermission | null = await requestPermission();
    if (!permission || permission !== "granted") return;

    return new Notification(title, options);
  };

  return { newNotification };
};
