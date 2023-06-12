
const storage = sessionStorage;

export function getItemOrDefault(key, defaultValue) {
    const stored = storage.getItem(key);
    if (!stored) {
        return defaultValue;
    }
    return JSON.parse(stored);
}

export function removeItem(key) {
    storage.removeItem(key);
}

export function setItem(key, value) {
    storage.setItem(key, JSON.stringify(value));
}
