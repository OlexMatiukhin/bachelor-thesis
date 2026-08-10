export function detectKind(file) {
    const name = (file.name || "").toLowerCase();
    if (/\.(png)$/.test(name)) return "image";
    if (/\.(wav)$/.test(name)) return "audio";
    return "other";
}