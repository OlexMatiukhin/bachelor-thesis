export function abortDownload(zone){
        if(zone.__reader){
            zone.__reader.abort(); 
        }
        URL.revokeObjectURL(zone.__objectUrl);
        zone.__objectUrl=null;
}
