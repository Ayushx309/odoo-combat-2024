/* Show Nav Bar */

const showMenu = (headerToggle, navbarId) =>{
    const toggleBtn = document.getElementById(headerToggle),
    nav = document.getElementById(navbarId)
    
   
    if(headerToggle && navbarId){
        toggleBtn.addEventListener('click', ()=>{
           
            nav.classList.toggle('show-menu')
         
            toggleBtn.classList.toggle('bx-x')
        })
    }
}
showMenu('header-toggle','navbar')

/* link active */
const linkColor = document.querySelectorAll('.nav_link')

function colorLink(){
    linkColor.forEach(l => l.classList.remove('active'))
    this.classList.add('active')
}

linkColor.forEach(l => l.addEventListener('click', colorLink))



