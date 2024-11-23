const inlineElements = document.querySelectorAll('.inline-group')
const $userRoleSwitcher = document.getElementsByClassName('field-type')[0].querySelector('select#id_type');
currentUserRole = $userRoleSwitcher.value
for($inlineElement of inlineElements){
    if($inlineElement.id ==`${currentUserRole}-group`){
        $currentFieldSet=$inlineElement
    }else{
        turnOffFieldSet($inlineElement)
    }
}

$userRoleSwitcher.addEventListener('change',(e)=>{
    if(currentUserRole == $userRoleSwitcher.value){
        return
    }
    turnOffFieldSet($currentFieldSet)
    currentUserRole = $userRoleSwitcher.value
    $currentFieldSet = document.getElementById(`${currentUserRole}-group`)
    turnOnFieldSet($currentFieldSet)
    }
)

function turnOffFieldSet($fieldSetName){
    let fieldsArray = $fieldSetName.querySelector('.inline-related').getElementsByClassName('flex-container')
    for($inputDiv of fieldsArray){
        $inputField = $inputDiv.lastElementChild
        if($inputField.tagName == 'INPUT'){
            $inputField.value = ''
        }else{
            $inputField.selectedIndex = 0
        }
    }

    $fieldSetName.setAttribute('hidden', '')
}

function turnOnFieldSet($fieldSetName){
    $fieldSetName.removeAttribute('hidden', '')
}