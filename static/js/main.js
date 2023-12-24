
function getCookie(name) {
  // Check if the requested cookie is the CSRF token
  if (name === 'csrftoken') {
    var csrfInput = document.querySelector('input[name="csrfmiddlewaretoken"]');
    if (csrfInput) {
      // Extract and return the CSRF token from the input value
      return csrfInput.value;
    }
  }

  var cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    var cookies = document.cookie.split(';');
    for (var i = 0; i < cookies.length; i++) {
      var cookie = cookies[i].trim();
      // Check if this cookie name is the one we are looking for
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }

  return cookieValue;
}


// $(document).ready(function () {
//   $('#comeanalyze').on('input', function () {
//     localStorage.removeItem('future-url');

//     var currentValue = $(this).val();
//     const v = localStorage.getItem('opt-url');
//     const p = sessionStorage.getItem('public-Token');

//     const imgssid1 = $('#processedImage');
//     const pImage = $('#pImage');

//     var csrftoken = getCookie('csrftoken');
//     success("Image is Analyzing ...");
//     $.ajax({
//       type: 'POST',
//       url: '/public/rlab', 

//       data: { 'confidence': currentValue, 'file': v, 'token': p }, 

//       success: function (response) {
//         imgssid1.attr('src', response.url); 
//         imgssid1.css('display', 'block'); 

//         localStorage.setItem('url', response.url)


//       },
//       error: function (xhr, status, error) {
//         errorInfo(error);

//       }
//     });
//   });
// });


$(document).ready(function () {
  $('#generatepdf').click(function (e) {
    e.preventDefault(); // Prevent the default form submission behavior

    const formData = new FormData($('#form2')[0]);

    const publicToken = sessionStorage.getItem('public-Token');

    if (publicToken) {
      formData.append('token', publicToken);
    }

    const currentDate = new Date();
    const currentDateTimeString = currentDate.toISOString();
    //var csrftoken = getCookie('csrftoken');
    formData.append('currentDateTime', currentDateTimeString);


    $.ajax({
      type: 'POST',
      url: '/public/r-generate_report',
      data: formData,
      processData: false,
      contentType: false,
      responseType: 'blob', // Expect binary data as blob


      success: function (response) {
        success("You Report link has sent to your mail");
	console.log(response);

      },
      error: function (xhr, status, error) {
        console.log(error);

        errorpop(error);
      }

    });
  });
});




$(document).ready(function () {

  var url = localStorage.getItem('url');

  const imgssid1 = $('#processedImage');
  const pImage = $('#pImage');
  if (url) {
    imgssid1.css('display', 'block');
    pImage.css('display', 'none');

    imgssid1.attr('src', url);
  } else {
    imgssid1.css('display', 'none');
    pImage.css('display', 'block');
  }

});
function success(suc) {

  Swal.fire({
    position: "top-end",
    icon: "success",
    title: "Thankyou!",
    text: suc,
    showConfirmButton: false,
    timer: 5000
  });
}
function errorpop(err) {
  Swal.fire({
    icon: "error",
    title: "Oops...",
    text: err,
  });
}





VanillaTilt.init(document.querySelector("#image-comparison-slider"), { // Tilt Effect - vanilla-tilt.js (https://micku7zu.github.io/vanilla-tilt.js/) is required for this
  max: 5, // max tilt rotation (degrees (deg))
  speed: 800, // speed (transition-duration) of the enter/exit transition (milliseconds (ms))
  scale: 1.02 // transform scale - 2 = 200%, 1.5 = 150%, etc..
});

const slider = document.querySelector("#image-comparison-slider");
const sliderImgWrapper = document.querySelector("#image-comparison-slider .img-wrapper");
const sliderHandle = document.querySelector("#image-comparison-slider .handle");

slider.addEventListener("mousemove", sliderMouseMove);
slider.addEventListener("touchmove", sliderMouseMove);

function sliderMouseMove(event) {

  if(isSliderLocked) return;

  const sliderLeftX = slider.offsetLeft;
  const sliderWidth = slider.clientWidth;
  const sliderHandleWidth = sliderHandle.clientWidth;

  let mouseX = (event.clientX || event.touches[0].clientX) - sliderLeftX;
  if(mouseX < 0) mouseX = 0;
  else if(mouseX > sliderWidth) mouseX = sliderWidth;

  sliderImgWrapper.style.width = `${((1 - mouseX/sliderWidth) * 100).toFixed(4)}%`;
  sliderHandle.style.left = `calc(${((mouseX/sliderWidth) * 100).toFixed(4)}% - ${sliderHandleWidth/2}px)`;
}

let isSliderLocked = false;

slider.addEventListener("mousedown", sliderMouseDown);
slider.addEventListener("touchstart", sliderMouseDown);
slider.addEventListener("mouseup", sliderMouseUp);
slider.addEventListener("touchend", sliderMouseUp);
slider.addEventListener("mouseleave", sliderMouseLeave);

function sliderMouseDown(event) {
  if(isSliderLocked) isSliderLocked = false;
  sliderMouseMove(event);
}

function sliderMouseUp() {
  if(!isSliderLocked) isSliderLocked = true;
}

function sliderMouseLeave() {
  if(isSliderLocked) isSliderLocked = false;
}