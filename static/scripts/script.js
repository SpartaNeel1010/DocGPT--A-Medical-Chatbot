console.log("Hello");
document.getElementById('newConvo').addEventListener('click',()=>{
  window.location.href="/new"
})

lefts = document.getElementsByClassName('left')
rights = document.getElementsByClassName('right')

for (let i = 0; i < lefts.length; i++) {
  lefts[i].addEventListener('click', generate)
}
for (let i = 0; i < rights.length; i++) {
  rights[i].addEventListener('click', generate)
}
function generate(event) {
  inputText = document.getElementById('inputText')
  inputText.value = this.getElementsByClassName('example')[0].innerHTML.trim()
  console.log(inputText.value)
  let form = document.getElementById('suggestform')
  try {
    document.getElementsByClassName('inital')[0].setAttribute('style', 'display:none;');
  }
  catch (err) {
    console.log(err)
  }
  let board = document.getElementsByClassName('chat__conversation-board')[0]
  console.log(form)
  board.innerHTML += `<div class="chat__conversation-board__message-container reversed temporary">
    <div class="chat__conversation-board__message__person">
        <div class="chat__conversation-board__message__person__avatar"><img
                src="static/Image/Human_image.png" alt="Dennis Mikle" /></div>
        <span class="chat__conversation-board__message__person__nickname">Me</span>
    </div>
    <div class="chat__conversation-board__message__context">
        <div class="chat__conversation-board__message__bubble">
            <h4>
                ${form.getElementsByClassName('finput')[0].value}
            </h4>
        </div>
    </div>
    </div>
    <div class="chat__conversation-board__message-container temporary">
    <div class="chat__conversation-board__message__person">
        <div class="chat__conversation-board__message__person__avatar"><img
                src="static/Image/bot_image.png" alt="Dennis Mikle" /></div>
        <span class="chat__conversation-board__message__person__nickname">Me</span>
    </div>
    <div class="chat__conversation-board__message__context">
        <div class="chat__conversation-board__message__bubble">
        <svg width="40" height="20" viewBox="0 0 40 20" xmlns="http://www.w3.org/2000/svg">
  <circle cx="10" cy="10" r="3" fill="#808080">
    <animate attributeName="r" values="3;6;3" dur="1s" repeatCount="indefinite"/>
  </circle>
  <circle cx="20" cy="10" r="3" fill="#808080">
    <animate attributeName="r" values="3;6;3" begin="0.2s" dur="1s" repeatCount="indefinite"/>
  </circle>
  <circle cx="30" cy="10" r="3" fill="#808080">
    <animate attributeName="r" values="3;6;3" begin="0.4s" dur="1s" repeatCount="indefinite"/>
  </circle>
</svg>


      
        </div>
    </div>
    </div>`
  document.body.appendChild(form);
  form.setAttribute('style', 'display:none;');
  form.submit()
}
document.getElementsByClassName('inp_form')[0].addEventListener('submit', handleForm);
// document.getElementsByClassName('inp_form_1')[0].addEventListener('submit',handleForm);
console.log("form")

function handleForm(event) {
  event.preventDefault();
  try {
    document.getElementsByClassName('inital')[0].setAttribute('style', 'display:none;');
  }
  catch (err) {
    console.log(err)
  }
  let board = document.getElementsByClassName('chat__conversation-board')[0]
  console.log(this)
  board.innerHTML += `<div class="chat__conversation-board__message-container reversed temporary">
    <div class="chat__conversation-board__message__person">
        <div class="chat__conversation-board__message__person__avatar"><img
                src="static/Image/Human_image.png" alt="Dennis Mikle" /></div>
        <span class="chat__conversation-board__message__person__nickname">Me</span>
    </div>
    <div class="chat__conversation-board__message__context">
        <div class="chat__conversation-board__message__bubble">
            <h4>
                ${this.getElementsByClassName('finput')[0].value}
            </h4>
        </div>
    </div>
    </div>
    <div class="chat__conversation-board__message-container temporary">
    <div class="chat__conversation-board__message__person">
        <div class="chat__conversation-board__message__person__avatar"><img
                src="static/Image/bot_image.png" alt="Dennis Mikle" /></div>
        <span class="chat__conversation-board__message__person__nickname">Me</span>
    </div>
    <div class="chat__conversation-board__message__context">
        <div class="chat__conversation-board__message__bubble">
        <svg width="40" height="20" viewBox="0 0 40 20" xmlns="http://www.w3.org/2000/svg">
  <circle cx="10" cy="10" r="3" fill="#808080">
    <animate attributeName="r" values="3;6;3" dur="1s" repeatCount="indefinite"/>
  </circle>
  <circle cx="20" cy="10" r="3" fill="#808080">
    <animate attributeName="r" values="3;6;3" begin="0.2s" dur="1s" repeatCount="indefinite"/>
  </circle>
  <circle cx="30" cy="10" r="3" fill="#808080">
    <animate attributeName="r" values="3;6;3" begin="0.4s" dur="1s" repeatCount="indefinite"/>
  </circle>
</svg>


      
        </div>
    </div>
    </div>`
  this.submit()
  inputText.setAttribute('style', 'display:none;');
  inputText = document.getElementById('inputText')
}


conversations=document.getElementsByClassName('conversation')

for (let i = 0; i < conversations.length; i++) {
  conversations[i].addEventListener('click', ()=>{
    id=conversations[i].id
    window.location.href = `/convo/${id}`;
  })
}
scrollableDiv=document.getElementsByClassName('chat__conversation-board')[0]
scrollableDiv.scrollTop = scrollableDiv.scrollHeight;

document.getElementById("createbtn").addEventListener('click',()=>{window.location="/create"})
document.getElementsByClassName("navimage")[0].addEventListener('click',()=>{window.location="/"})

function myFunction() {
  document.getElementById("myDropdown").classList.toggle("show");
}

// Close the dropdown menu if the user clicks outside of it
window.onclick = function(event) {
  if (!event.target.matches('.dropbtn')) {
    var dropdowns = document.getElementsByClassName("dropdown-content");
    var i;
    for (i = 0; i < dropdowns.length; i++) {
      var openDropdown = dropdowns[i];
      if (openDropdown.classList.contains('show')) {
        openDropdown.classList.remove('show');
      }
    }
  }
}

micbtn=document.getElementById("micBtn")
recbtn=document.getElementById("recBtn")
micbtn.addEventListener('click',function(){
  micbtn.setAttribute('style','display:none');
  recbtn.setAttribute('style','display:inline');
  var speech = true;
  window.SpeechRecognition = window.webkitSpeechRecognition;

  const recognition = new SpeechRecognition();
  recognition.interimResults = true;
  recognition.continuous = true; // Allow continuous recognition

  // Set the desired speech timeout (in milliseconds)
  recognition.speechTimeout = 3000; 

  recognition.addEventListener('result', e => {
      const transcript = Array.from(e.results)
          .map(result => result[0])
          .map(result => result.transcript)
          .join('')

      document.getElementById("inp_text").value = transcript;
      console.log(e.results)
      console.log(transcript);
      if(e.results[0]['isFinal'])
      {
        micbtn.setAttribute('style','display:inline');
        recbtn.setAttribute('style','display:none');
      }
  });
  
  if (speech == true) {
      recognition.start();
  }
})


const speakBtn = document.getElementById('speakBtn');
let p=true

let utterance = new SpeechSynthesisUtterance();

speakBtn.addEventListener('click', () => {
    if(p)
    {
      text=speakBtn.parentNode.parentNode.getElementsByTagName('h4')[0].innerHTML
      text=text.replace("<br>","\n")
      utterance.text = text
      console.log(text)
      speechSynthesis.speak(utterance);
      p=false
      
    }
    else
    {
      speechSynthesis.cancel();
      p=true;
    }
});


