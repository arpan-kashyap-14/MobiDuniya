

// const outputVoice = (txt) => {
//   const msg = new SpeechSynthesisUtterance();
//   msg.text = `${txt}`;
//   window.speechSynthesis.speak(msg);
// }

// for (var i = 0; i < langs.length; i++) {
//   select_language.options[i] = new Option(langs[i][0], i);
// }
// select_language.selectedIndex = 6;
// updateCountry();
// select_dialect.selectedIndex = 6;

const outputVoice = (txt) => {
  const msg = new SpeechSynthesisUtterance();
  msg.text = `${txt}`;
  window.speechSynthesis.speak(msg);
}

showInfo('info_start');

// function updateCountry() {
//   for (var i = select_dialect.options.length - 1; i >= 0; i--) {
//     select_dialect.remove(i);
//   }
//   var list = langs[select_language.selectedIndex];
//   for (var i = 1; i < list.length; i++) {
//     select_dialect.options.add(new Option(list[i][1], list[i][0]));
//   }
//   select_dialect.style.visibility = list[1].length == 1 ? 'hidden' : 'visible';
// }

// var create_email = false;

var final_transcript = '';
var recognizing = false;
var ignore_onend;
var start_timestamp;



if (!('webkitSpeechRecognition' in window)) {
  upgrade();
} else {
  start_button.style.display = 'inline-block';
  var recognition = new webkitSpeechRecognition();
  recognition.continuous = true;
  recognition.interimResults = true;

  // voice on start
  recognition.onstart = function() {
    recognizing = true;
    showInfo('info_speak_now');
    start_img.src = `../../static/app/images/voice/mic-animate.gif`;
  };

  // voice on error
  recognition.onerror = function(event) {
    if (event.error == 'no-speech') {
      start_img.src = `../../static/app/images/voice/mic.gif`;
      showInfo('info_no_speech');
      ignore_onend = true;
    }
    if (event.error == 'audio-capture') {
      start_img.src = `../../static/app/images/voice/mic.gif`;
      showInfo('info_no_microphone');
      ignore_onend = true;
    }
    if (event.error == 'not-allowed') {
      if (event.timeStamp - start_timestamp < 100) {
        showInfo('info_blocked');
      } else {
        showInfo('info_denied');
      }
      ignore_onend = true;
    }
  };

  // voice on end
  recognition.onend = function() {
    recognizing = false;
    if (ignore_onend) {
      return;
    }
    start_img.src = `../../static/app/images/voice/mic.gif`;
    if (!final_transcript) {
      showInfo('info_start');
      return;
    }
    showInfo('');
    if (window.getSelection) {
      window.getSelection().removeAllRanges();
      var range = document.createRange();
      range.selectNode(document.getElementById('final_span'));
      window.getSelection().addRange(range);
    }

    // if (create_email) {
    //   create_email = false;
    //   createEmail();
    // }

    // alert(final_transcript); 
     if(final_transcript != ""){
       $('#final_span').attr('value',`${final_transcript}`);
       
       reqData = {text:final_transcript}

       $.ajax({
         type:"GET",
         url:"/search",
         contentType:"application/json",
         data:reqData,
         success:function(data){

            if(data.resData == "render_cart"){
                window.location.href = "/cart";
            }
            if(data.productId != null){
              pid = data.productId
              window.location.href = `product-detail/${pid}`;
            }
         
            if(data.brandName != null){
              b = data.brandName
              brand_name = b.toLowerCase();  
              window.location.href = `/${brand_name}`;
            }
             

            if(data.user == "userProfile"){
              window.location.href = "/user";
            }
            if(data.cart == "userCart"){
                window.location.href = "/cart"
            }
            if(data.suggest == "userSuggest"){
              window.location.href="/suggest";
            }  
            if(data.compare == "userCompare"){
              window.location.href ="/compare"
            }
            if(data.password == "userPassword"){
              window.location.href = "/passwordchange"
            }
            if(data.home == "userHome"){
              window.location.href = "/" 
            }
            if(data.logout == "userLogout"){
              window.location.href = "/logout"
            }
            if(data.default == "userDefault"){
              
                // outputVoice(`Please try another query`);
                alert("hello")
                    
            }

         },
         error:function(error){
           console.log(error); 
         }

       });
       
     }

  };

  // voice on result
  recognition.onresult = function(event) {
    var interim_transcript = '';
    for (var i = event.resultIndex; i < event.results.length; ++i) {
      if (event.results[i].isFinal) {
        final_transcript += event.results[i][0].transcript;
      } else {
        interim_transcript += event.results[i][0].transcript;
      }
    }
    final_transcript = capitalize(final_transcript);
    final_span.innerHTML = linebreak(final_transcript);
    // interim_span.innerHTML = linebreak(interim_transcript);

    if (final_transcript || interim_transcript) {
      showButtons('inline-block');
    }
  };
}

function upgrade() {
  start_button.style.visibility = 'hidden';
  showInfo('info_upgrade');
}

var two_line = /\n\n/g;
var one_line = /\n/g;
function linebreak(s) {
  return s.replace(two_line, '<p></p>').replace(one_line, '<br>');
}

var first_char = /\S/;
function capitalize(s) {
  return s.replace(first_char, function(m) { return m.toUpperCase(); });
}


// function createEmail() {
//   var n = final_transcript.indexOf('\n');
//   if (n < 0 || n >= 80) {
//     n = 40 + final_transcript.substring(40).indexOf(' ');
//   }
//   var subject = encodeURI(final_transcript.substring(0, n));
//   var body = encodeURI(final_transcript.substring(n + 1));
//   window.location.href = 'mailto:?subject=' + subject + '&body=' + body;
// }

// function copyButton() {
//   if (recognizing) {
//     recognizing = false;
//     recognition.stop();
//   }
//   copy_button.style.display = 'none';
//   copy_info.style.display = 'inline-block';
//   showInfo('');
// }

// function emailButton() {
//   if (recognizing) {
//     create_email = true;
//     recognizing = false;
//     recognition.stop();
//   } else {
//     createEmail();
//   }
//   email_button.style.display = 'none';
//   email_info.style.display = 'inline-block';
//   showInfo('');
// }


function startButton(event) {
  if (recognizing) {
    recognition.stop();
    return;
  }
  final_transcript = '';
  recognition.lang = 'en-IN';
  recognition.start();
  ignore_onend = false;
  final_span.innerHTML = '';
  // interim_span.innerHTML = '';
  start_img.src = `../../static/app/images/voice/mic-slash.gif`;
  showInfo('info_allow');
  showButtons('none');
  start_timestamp = event.timeStamp;
}


// show messages 
function showInfo(s) {
  if (s) {
    for (var child = info.firstChild; child; child = child.nextSibling) {
      if (child.style) {
        child.style.display = child.id == s ? 'inline' : 'none';
      }
    }
    info.style.visibility = 'visible';
  } else {
    info.style.visibility = 'hidden';
  }
}

var current_style;
function showButtons(style) {
  if (style == current_style) {
    return;
  }
  current_style = style;
  // copy_button.style.display = style;
  // email_button.style.display = style;
  // copy_info.style.display = 'none';
  // email_info.style.display = 'none';
}



// search on click

const searchContent = (e) =>{
  
  const searchVal = $("#final_span").val();

  if(searchVal != ""){

    reqData = {text:searchVal}

    $.ajax({
      type:"GET",
      url:"/search",
      contentType:"application/json",
      data:reqData,
      success:function(data){

         if(data.resData == "render_cart"){
             window.location.href = "/cart";
         }
         else if(data.productId != null){
           pid = data.productId
           window.location.href = `product-detail/${pid}`;
         }
      
         else if(data.brandName != null){
           b = data.brandName
           brand_name = b.toLowerCase();  
           window.location.href = `/${brand_name}`;
         }
         else if(data.user == "userProfile"){
           window.location.href = "/user";
         }
         else if(data.cart == "userCart"){
             window.location.href = "/cart"
         }
         else if(data.suggest == "userSuggest"){
           window.location.href="/suggest";
         }  
         else if(data.compare == "userCompare"){
           window.location.href ="/compare"
         }
         else if(data.password == "userPassword"){
           window.location.href = "/passwordchange"
         }
         else if(data.home == "userHome"){
           window.location.href = "/" 
         }
         else if(data.logout == "userLogout"){
           window.location.href = "/logout"
         }else{

             outputVoice("Please Try Another Query") 
         }

      },
      error:function(error){
        console.log(error); 
      }

    });

  }else{
    
     outputVoice("Please fill the search Box");
  }


}