const MAGIC = new TextEncoder().encode("CHAOSENC");
export async function checkFileMarker(file) {
    const tail = file.slice(Math.max(0, file.size - 300));
    const buffer = await tail.arrayBuffer();
    const bytes = new Uint8Array(buffer);
    const view = new DataView(buffer);

    if (bytes.length < 4) return null;
    const markerSize = view.getUint32(bytes.length - 4, false);

    if (markerSize > file.size || markerSize < MAGIC.length + 1 + 1 + 8 + 4) return null;
    const markerStart = bytes.length - markerSize;
    if (markerStart < 0) return null;

    for (let i = 0; i < MAGIC.length; i++) {
        if (bytes[markerStart + i] !== MAGIC[i]) return null;
    }

    let offset = markerStart + MAGIC.length;
    const version = bytes[offset++];
    const nameLen = bytes[offset++];
    const timestamp = Number(view.getBigUint64(offset, false));
    offset += 8;
    const filename = new TextDecoder().decode(
        bytes.slice(offset, offset + nameLen)
    );

    return {
        isEncrypted: true,
        version,
        filename,
        encryptedAt: new Date(timestamp * 1000).toLocaleString("uk-UA"),
    };
}