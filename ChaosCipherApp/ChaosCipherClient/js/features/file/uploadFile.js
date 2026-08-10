//-------------------------------Upload File on Server--------------------------------------------------
import { buildRequestFormData } from "../formData/getFromData.js";
import { getVisibleBlock } from "../dataBlock/getVisibleBlock.js";
import { getUrlByBlockIdAndProcessType } from "./getUrlByBlockIdAndProcessType.js";
import { setErrorInDataBlock, setProgressBarInDataBlock } from "../dataBlock/setProgressAndErrorBlock.js";
import { bindProcessedFile } from "./readFile.js";
import { shouldDisableHeaderElements } from "../header/headerBlock.js";
import { resetProcessedResultByZone } from "./readFile.js";
export function uploadStoredFile(zone, operation, btn) {
    parent = btn.parentElement.parentElement.parentElement;
    resetProcessedResultByZone(parent);
    const file = zone.selectedFile;
    if (!file) {
        setErrorInDataBlock(zone, "Оберіть файл перед відправкою", true)
        return;
    }

    const formData = buildRequestFormData();
    if (!formData) return
    const dataBlock = getVisibleBlock();
    let chosen_URL = "";
    let data_type = "";
    if (!dataBlock) return
    setErrorInDataBlock(dataBlock, "", false);
    let result = getUrlByBlockIdAndProcessType(dataBlock.id, operation)
    chosen_URL = result.chosen_URL;
    data_type = result.data_type
    formData.append("data_type", data_type)
    formData.append("file", file)

    const xhr = new XMLHttpRequest();
    zone.__xhr = xhr;
    xhr.open("POST", chosen_URL, true);
    shouldDisableHeaderElements(true);
    xhr.responseType = 'blob';
    xhr.upload.addEventListener("progress", (e) => {
        if (!e.lengthComputable) return
        let pct = Math.round((e.loaded / e.total) * 100)
        setProgressBarInDataBlock(dataBlock, pct, true);
    })
    xhr.addEventListener("load", async () => {
        if (xhr.status >= 200 && xhr.status < 300) {
            const blob = xhr.response;
            // Extract extension from Content-Disposition: filename="processed.docx"
            const disposition = xhr.getResponseHeader("Content-Disposition") || "";
            const match = disposition.match(/filename[^;=\n]*=["']?[^.]+\.([^"';\n]+)/);
            const ext = match ? match[1] : null;
            shouldDisableHeaderElements(false);
            bindProcessedFile(blob, ext);
            setProgressBarInDataBlock(dataBlock, 100, true);
            setTimeout(() => { setProgressBarInDataBlock(dataBlock, 0, false) }, 500);


        }
        else {
                shouldDisableHeaderElements(false);
                let errorMessage = "Помилка при відправці даних на сервер.";

                try {
                    if (xhr.response) {                        
                        const text = await xhr.response.text();
                        const parsed = JSON.parse(text);
                        if (parsed.detail) errorMessage = parsed.detail;
                    }
                } catch (e) {
                    console.error("Error parsing server response:", e);
                }
                setErrorInDataBlock(dataBlock, errorMessage, true); 
                setProgressBarInDataBlock(dataBlock, 0, false);
        }
    })

    xhr.addEventListener("error", () => {
        shouldDisableHeaderElements(false);
        setProgressBarInDataBlock(dataBlock, 0, false)
        setErrorInDataBlock(dataBlock, "Помилка при відправці даних на сервер.", true);
    })
    xhr.addEventListener("abort", () => {
        shouldDisableHeaderElements(false);
        setProgressBarInDataBlock(dataBlock, 0, false);
        setErrorInDataBlock(dataBlock, "", false);
    });
    xhr.send(formData);



}
