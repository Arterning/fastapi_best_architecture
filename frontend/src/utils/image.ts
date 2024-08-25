

export const getPreviewURL = (obj_name: string) => {
    const { origin } = window.location;
    if (!obj_name) {
      obj_name = "pe.jpg";
    }
    const BASE = import.meta.env.VITE_API_BASE_URL;
    if (BASE) {
      return `${BASE}/api/v1/data/attachement/preview/${obj_name}`;
    }
    return `${origin}/api/v1/data/attachement/preview/${obj_name}`;
};