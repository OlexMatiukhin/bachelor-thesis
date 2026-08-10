import { API } from "../../config.js";
import { buildRequestFormData } from "../formData/getFromData.js";
import { setErrorInDataBlock, setProgressBarInDataBlock } from "../dataBlock/setProgressAndErrorBlock.js";
import { setInputTextError, setResultInputError } from "../text/setTextError.js"
import {updateCharCount } from "../text/initText.js"
export function uploadText(zone, operation) {
    const originalText = document.getElementById("original-text-content").value;
    const processedText = document.getElementById("processed-text-content");
    const textBlock = document.getElementById("encrypt-text");
    setErrorInDataBlock(textBlock, "", false);
    setResultInputError("", false);

    if (!originalText) {
        setInputTextError("Введіть текст перед відправкою", true)
        return
    }
    const formData = buildRequestFormData();
    if (!formData) return
    formData.set("operation", operation);
    formData.append("data_type", "text")
    formData.set("text", originalText)
    const xhr = new XMLHttpRequest();
    zone.__xhr = xhr;
    if (operation == "Encrypt") {
        xhr.open("POST", API.ENCRYPT_TEXT_URL, true);
    }
    else if (operation == "Decrypt") {
        xhr.open("POST", API.DECRYPT_TEXT_URL, true);
    }



    xhr.upload.addEventListener("progress", (e) => {
        if (!e.lengthComputable) return
        let pct = Math.round((e.loaded / e.total) * 100)
        setProgressBarInDataBlock(textBlock, pct, true);
    })
    xhr.addEventListener("load", () => {
        if (xhr.status === 200) {
            const response = JSON.parse(xhr.responseText);
            
            processedText.value = response.processed_text;
            updateCharCount("processed-text-content", "out-char-count");
            setProgressBarInDataBlock(textBlock, 100, true);
            setTimeout(() => { setProgressBarInDataBlock(textBlock, 0, false) }, 500);

        }

        else {
            setProgressBarInDataBlock(textBlock, 0, false)
            let errorMessage ="Помилка при відправці даних на сервер.";
            try {
                const response = JSON.parse(xhr.responseText);
                if (response.detail) {
                    errorMessage = response.detail;
                }
                setResultInputError(errorMessage, true);
                document.getElementById("out-char-count").textContent = "0 символів";
            }

            catch (e) {
                console.error("Error parsing server response:", e);
            }
        }
    })

    xhr.addEventListener("error", () => {
        console.error("Error during text upload:", xhr.statusText);
        setProgressBarInDataBlock(textBlock, 0, false)
        setResultInputError(`Помилка при відправці даних на сервер. Відсутній доступ або ж сервер тимчасово не працює.`, true);
        document.getElementById("out-char-count").textContent = "0 символів";
    })
    xhr.addEventListener("abort", () => {
        setProgressBarInDataBlock(textBlock, 0, false);
        setErrorInDataBlock(textBlock, "", false);
    });
    return xhr.send(formData);


}  
