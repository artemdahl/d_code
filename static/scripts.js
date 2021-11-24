document.addEventListener("DOMContentLoaded", function(){
    let btn = document.querySelector('input[type=submit]');
    btn.addEventListener('click', async function(event){
        event.preventDefault();
        let new_word = document.querySelector('input[name=new_word]').value;
        if (new_word == '') {
            return
        }
        let response = await fetch("/", {
            method: "POST",
            body: new FormData(document.querySelector('.form_new_word')) 
        }) 
        let response_json = await response.json();
        if (response_json.success){ 
            let message = document.querySelector('.message');
            message.innerHTML = response_json.message;
        }
        else {
            return
        }
    })
})
