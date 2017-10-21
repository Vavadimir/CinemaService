// Dropzone.autoDiscover = false;
//
//         var myDropzone = new Dropzone('#post_img', {
//           url: "/poster/",
//           autoProcessQueue: false,
//           addRemoveLinks: true,
//           init: function() {
//               this.on("sending", function (file, xhr, formData) {
//                   formData.append("title", $('input[name=title]').val());
//                   formData.append("premiere_date", $('input[name=premiere_date]').val());
//               });
//           },
//         });
//
//         $('#submit_post').click(function(){
//           myDropzone.processQueue();
//         });