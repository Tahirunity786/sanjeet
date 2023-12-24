// function scrollToProcess() {
//   var processSection = document.getElementById("process");
//   if (processSection) {
//     processSection.scrollIntoView({ behavior: "smooth" }); // You can also use "auto" for instant scroll
//   }
// }



// if (UrlStorage) {
//   // If it exists, hide the 'nesimage' and 'animationimage' elements
//   nesimage.style.display = "none";
//   animationimage.style.display = "none";

//   // Set the 'src' attribute of 'imgssid1' with the value from localStorage
//   imgssid1.attr('src', UrlStorage);
//   imgssid1.css('display', 'block');
//   $('#generatepdf').prop('disabled', false);
//   $('#comeanalyze').prop('disabled', false);
// }
// else{
//   imgssid1.css('display', 'none');
//   nesimage.style.display = "none";
//   imagehandle.innerText="Please Upload an Image"
// }


// $(document).ready(function () {
//   $('#analyzeme').click(function () {
//     localStorage.removeItem('future-url');

//     // Hide the image
//     $('#imgssid1').css('display', 'none');
//     scrollToProcess();
//     // Reset any previous error messages
//     $('#error-message').remove();

//     // Validate email
//     const email = $('#exampleInputEmail1').val();
//     if (!isValidEmail(email)) {
//       $('#exampleInputEmail1').after('<p id="error-message" class="text-danger">Invalid email address</p>');
//       return;
//     }

//     // Validate file
//     const fileInput = $('#inputGroupFile02')[0];
//     if (fileInput.files.length === 0) {
//       $('#inputGroupFile02').after('<p id="error-message" class="text-danger">Please select a file</p>');
//       return;
//     }

//     // If email and file are valid, continue with the AJAX request

//     //STYLE SECTION
//     const formData = new FormData($('#myForm')[0]);
//     const imgssid1 = $('#imgssid1');
//     const nesimage = $('#nesimage');
//     const animationimage = $('#animationimage');
//     imagehandle.style.display = "none";
//     nesimage.css('display', 'none');
//     animationimage.css('display', 'block');

//     $.ajax({
//       type: 'POST',
//       url: '/public/lab', // Replace with your server endpoint
//       data: formData,
//       processData: false,
//       contentType: false,
//       success: function (response) {
//         // STYLING ELEMENT
//         imgssid1.attr('src', response.url); // Use .attr() method
//         imgssid1.css('display', 'block'); // Use .css() method
//         animationimage.css('display', 'none'); // Use .css() method
//         $('#generatepdf').prop('disabled', false);
//         $('#comeanalyze').prop('disabled', false);

//         // TEMPPORARY SETTIGS
//         sessionStorage.setItem('public-Token', response.session_token)
//         localStorage.setItem('future-url', response.url)
//         localStorage.setItem('opt-url-url', response.opt_url)
//       },
//       error: function (xhr, status, error) {
//         // Handle any other errors

//         errorInfo(error);
//         animationimage.css('display', 'none');
//         nesimage.css('display', 'block');
//         $('#imgssid1').css('display', 'none');
//       }
//     });
//   });
// });

// function onClick(e) {
//   e.preventDefault();
//   grecaptcha.ready(function () {
//     grecaptcha.execute('6LdXn9coAAAAAFpyP6AlyHUUJxn0izL1xqUPBLTC', { action: 'submit' }).then(function (token) {
//       // Add your logic to submit to your backend server here.
//     });
//   });
// }