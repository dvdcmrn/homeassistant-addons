const PREFIX = "sf";
const BASE = "/cupertino-icons";

async function getIcon(name) {
  const response = await fetch(`${BASE}/icon/${encodeURIComponent(name)}`);
  if (!response.ok) {
    return { path: "", viewBox: "0 0 24 24" };
  }
  return response.json();
}

async function getIconList() {
  const response = await fetch(`${BASE}/list`);
  if (!response.ok) {
    return [];
  }
  return response.json();
}

window.customIcons = window.customIcons || {};
window.customIcons[PREFIX] = { getIcon, getIconList };
