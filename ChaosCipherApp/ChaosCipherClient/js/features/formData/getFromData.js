    import { validateActiveParams } from "../formData/validateActiveParams.js";

    export function buildRequestFormData(){
        const formData = new FormData();
        const validation = validateActiveParams();
        if(!validation.validationPassed){
            return null
        }
        const menuContainer = document.getElementById('menuContainer');
        const menuContainerSelects = menuContainer.querySelectorAll("select");
                menuContainerSelects.forEach(select=>{
            formData.append(select.name, select.value);
        })   
       
        formData.append("params", JSON.stringify(validation.paramsObj));
        return formData;
    }
