export function getActiveParamBlock(){
      const systemSelect = document.getElementById('system');
      const activeId = systemSelect.value;
      const activeParamBlock = document.getElementById(`${activeId}-params`);
      return activeParamBlock;
}

function showValidationError(input, message) {
    const group = input.closest('.form-group');
    if (group) {
        const old = group.querySelector('.param-error');
        if (old) old.remove();

        const errEl = document.createElement('small');
        errEl.className = 'param-error';
        errEl.textContent = message;
        group.appendChild(errEl);
    }
    input.classList.add('input-error');
    input.focus();
}

function clearValidationErrors(block) {
    block.querySelectorAll('.param-error').forEach(el => el.remove());
    block.querySelectorAll('.input-error').forEach(el => el.classList.remove('input-error'));
}
function parseNumberInput(input) {
    const raw = (input.value ?? "").trim().replace(",", ".");
    const value = Number(raw);
    return { raw, value };
}

const blockRules = {
    "lorenz-params": {
        logisticXLorenz: { min: 0, max: 1,},  
        lorenzX: { min: -20, max: 20 },
        lorenzY: { min: -20, max: 20 },
        lorenzZ: { min: 0, max: 60 }
    },

    "rossler-params": {
        logisticXRossler: { min: 0, max: 1,},  
        rosslerX: { min: -15, max: 15 },
        rosslerY: { min: -15, max: 15 },
        rosslerZ: { min: 0, max: 25 }
    },

    "chua-params": {
        logisticXChua: { min: 0, max: 1,},  
        chuaX: { min: -3, max: 3 },
        chuaY: { min: -2, max: 2 },
        chuaZ: { min: -3, max: 3 }
    },

    "duffing-params": {
        logisticXDuffing: { min: 0, max: 1,}, 
        duffingX: { min: -2, max: 2 },
        duffingY: { min: -2, max: 2 },
        duffingT: { min: 0, max:undefined }
    },

    "pol-params": {
        logisticXPol: { min: 0, max: 1,}, 
        polX: { min: -3, max: 3 },
        polY: { min: -8, max: 8 },
        polT: { min: 0, max:undefined }
    },

    "forced-params": {
        logisticXForced: { min: 0, max: 1,}, 
        forcedX: { min: -Math.PI, exclusiveMax: Math.PI }, 
        forcedY: { min: -6, max: 6 },  
        forcedT:  { min: 0, max:undefined }               
    }
};

function validateContinuousSystemParams(activeBlock, paramsObj) {
    const rules = blockRules[activeBlock.id];
    for (const [fieldName, limits] of Object.entries(rules)) {
        const input = activeBlock.querySelector(`[name="${fieldName}"]`);
       
       const { raw, value } = parseNumberInput(input);
       const digitsOnly = raw.replace(/[.,-]/g, "").replace(/\D/g, "");
       if (input.validity.badInput || raw === "" || !Number.isFinite(value)) {
            showValidationError(input, `"${fieldName}" має бути числом`);
            return { validationPassed: false, paramsObj: null };
        }
       
        const decimalPart = raw.includes(".") ? raw.split(".")[1] : "";

        if (decimalPart.length > 6) {
            showValidationError(input, `"${fieldName}" має мати не більше 6 цифр після коми`);
            return { validationPassed: false, paramsObj: null };
        }
        
        if (input.id.includes("logisticX")) {
            if (limits.min !== undefined && value <= limits.min) {
                showValidationError(
                    input,
                    `"${fieldName}" має бути більше ${limits.min}`
                );
                return { validationPassed: false, paramsObj: null };
            }
            if (limits.max !== undefined && value >= limits.max) {
                showValidationError(
                    input,
                    `"${fieldName}" має бути менше ${limits.max}`
                );
                return { validationPassed: false, paramsObj: null };
            }
        } else {
            if (limits.min !== undefined && value < limits.min) {
                showValidationError(
                    input,
                    `"${fieldName}" має бути не менше ${limits.min}`
                );
                return { validationPassed: false, paramsObj: null };
            }
            if (limits.exclusiveMax !== undefined && value >= limits.exclusiveMax) {
                showValidationError(
                    input,
                    `"${fieldName}" має бути менше ${limits.exclusiveMax}`
                );
                return { validationPassed: false, paramsObj: null };
            }
            if (limits.max !== undefined && value > limits.max) {
                showValidationError(
                    input,
                    `"${fieldName}" має бути не більше ${limits.max}`
                );
                return { validationPassed: false, paramsObj: null };
            }
        }
   
        paramsObj[fieldName] = value;
    }

    return { validationPassed: true, paramsObj };
}

export function validateActiveParams(){
    const activeBlock = getActiveParamBlock();
    const paramsObj = {};
    if(! activeBlock){
        alert("Немає видимого блоку з параметрами!")
        return {validationPassed: false, paramsObj:null}
    }
    clearValidationErrors(activeBlock);
    return validateContinuousSystemParams(activeBlock, paramsObj);
}