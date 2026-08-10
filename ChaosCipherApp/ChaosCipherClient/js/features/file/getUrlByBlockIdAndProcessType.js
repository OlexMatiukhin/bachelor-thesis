import { API } from "../../config.js";
const URL_MAP = {
    "encrypt-image": { encrypt: API.ENCRYPT_IMAGE_URL, decrypt: API.DECRYPT_IMAGE_URL, type: "image" },
    "encrypt-audio": { encrypt: API.ENCRYPT_AUDIO_URL, decrypt: API.DECRYPT_AUDIO_URL, type: "audio" },
    "encrypt-file":  { encrypt: API.ENCRYPT_FILE_URL,  decrypt: API.DECRYPT_FILE_URL,  type: "file"  },
};

export function getUrlByBlockIdAndProcessType(id, operation) {
    const entry = URL_MAP[id] ?? URL_MAP["encrypt-file"];
    return {
        chosen_URL: operation === "Encrypt" ? entry.encrypt : entry.decrypt,
        data_type: entry.type,
    };
}