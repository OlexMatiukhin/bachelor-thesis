export function setProgressBar(zone,value, show){
        const progressBlock = document.getElementsByClassName("dz-progress")[0];
        const progressBar = document.getElementsByClassName("dz-progress-bar")[0];
        if (!progressBlock || !progressBar) return;

        if(show){
            progressBlock.style.display="block";
            progressBar.style.display="block";
            let v=Math.max(0, Math.min(100, value));
            progressBar.style.width=`${v}%`
            console.log("Set value");
        }
        else{
            progressBlock.style.display="none";
            progressBar.style.display="none";
        }
}

export function setError(zone, value, show) {
    const errorBlock = document.getElementsByClassName('dz-error')[0];
    if (!errorBlock) return;
    errorBlock.style.display = show ? "block" : "none";
    errorBlock.textContent = show ? value : "";
}



/*export  function setError(zone,value, show){
        let error_block=document.getElementsByClassName('dz-error')[0];
        if(show){
            error_block.style.display="block";
            error_block.textContent=value;
        }
        else{
            error_block.style.display="none";
            error_block.textContent=value;
        }

}*/