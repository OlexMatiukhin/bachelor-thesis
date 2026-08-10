export function setupDownloadButtons() {
    const operationBlocks = document.querySelectorAll(".operation");

    operationBlocks.forEach((block) => {
        const downloadBtn = block.querySelector(".download-btn");
        if (!downloadBtn) return;

        downloadBtn.addEventListener("click", () => {
            try {
                downloadResultFromBlock(block);
            } catch (err) {
                console.error("Download error:", err);
                alert("Не вдалося завантажити файл");
            }
        });
    });
}

function downloadResultFromBlock(block) {
    const blockId = (block.id || "").toLowerCase();
    if (blockId.includes("image")) {
        downloadProcessedMedia(block, "image", ".processed-image-content");
        return;
    }
    if (blockId.includes("audio")) {
        downloadProcessedMedia(block, "audio", ".processed-audio-content");
        return;
    }
    if (blockId.includes("file")) {
        const fileLink = block.querySelector(".link-download-processed");
        if (!fileLink || !fileLink.href) {
            alert("Немає файлу для завантаження");
            return;
        }

        triggerUrlDownload(fileLink.href, makeDownloadFileName(block, "file"));
        return;
    }
    alert("Немає результату для завантаження");
}

function downloadProcessedMedia(block, type, mediaSelector) {
    const fileName = makeDownloadFileName(block, type);
    if (block.__fileBuffer) {
        downloadBlob(block.__fileBuffer, fileName);
        return;
    }
    if (block.__objectUrl) {
        triggerUrlDownload(block.__objectUrl, fileName);
        return;
    }
    downloadFromMediaSrc(block.querySelector(mediaSelector), fileName);
}

function downloadBlob(data, fileName) {
    const blob = data instanceof Blob ? data : new Blob([data]);
    const url = URL.createObjectURL(blob);
    triggerUrlDownload(url, fileName);
    setTimeout(() => URL.revokeObjectURL(url), 0);
}

function downloadFromMediaSrc(mediaEl, fileName) {
    if (!mediaEl) {
        alert("Елемент результату не знайдено");
        return;
    }
    const src = (mediaEl.src || mediaEl.currentSrc || "").trim();
    if (!src || src === window.location.href) {
        alert("Немає результату для завантаження");
        return;
    }
    triggerUrlDownload(src, fileName);
}

function triggerUrlDownload(url, fileName) {
    const a = document.createElement("a");
    a.href = url;
    a.download = fileName || "download";
    document.body.appendChild(a);
    a.click();
    a.remove();
}

function makeDownloadFileName(block, type) {
    const blockId = (block.id || "").toLowerCase();
    let base = "processed-result";
    if (blockId =="encrypt-image") base = "processed-image";
    else  if (blockId =="encrypt-audio") base = "processed-audio";
    else if (blockId =="encrypt-file") base = "processed-file";
    let ext = "bin";
    if (type === "image") ext = "png";
    else if (type === "audio") ext = "wav";  
    else if (type === "file") {
        const filename = block.dataset.originalFilename; 
        ext = filename?.split(".")?.pop().toLowerCase() || "";
    }
    return `${base}-${Date.now()}.${ext}`;
}  
