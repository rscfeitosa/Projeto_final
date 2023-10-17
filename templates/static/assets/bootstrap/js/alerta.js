(function(win,doc){
    'use strict';

//botão de verificação de delete
    if(doc.querySelector('.btnDel')){
        let btnDel = doc.querySelectorAll('.btnDel');
        for(let i=0; i < btnDel.length; i++){

            btnDel[i].addEventListener('click', function(event){
                if(confirm('Deseja mesmo apagar esse produto? ')){
                    return true;
                }else{
                    event.preventDefault();
                }
            });
        }
    }

})(window,document);