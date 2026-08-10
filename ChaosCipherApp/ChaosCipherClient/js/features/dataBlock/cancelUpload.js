export function cancelUpload(zone) {
    if (zone.__xhr) {
        zone.__xhr.abort();
        zone.__xhr = null;
    }
}