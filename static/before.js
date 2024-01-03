// <!-- Script for data fetching per seconds
// <script>
//     function editDate (dat){
//         formatD = new Date(dat)
//         d = ((formatD.getDate()<10)?"0"+formatD.getDate():formatD.getDate()) + "-" + 
//         ((formatD.getMonth()+1<10)?"0"+(formatD.getMonth()+1):(formatD.getMonth()+1)) + "-"+ formatD.getFullYear()
//         return d
//     }
//     setInterval(function()
//     {
//         $(document).ready(
//             function()
//             {
//                 $.ajax(
//                     {
//                         type : "GET",
//                         url : "/getmessage/{{userprofile.user.username}}",
//                         success: function(data)
//                         {
//                             $.each(data, function(ind, val){
//                                 $('.chat-cont').empty()
//                                 $.each(val, function(i ,value){
//                                     c=value[1]
//                                     b= parseInt("{{userprofile.user.id}}")
//                                     //console.log(value)
//                                     if (b===c){
//                                         const p = `<div class="d-flex justify-content-center my-2 text-dark"><small style="font-size:12px;">${formatDate(value[5])}</small></div>
//                                         <div class="profile-cont p-3 mb-3 d-flex">
//                                             <a href="{% url 'profile' userprofile.user.username %}" class="text-decoration-none text-white">
//                                               <div class="chat-buddy" style="width: 60px; height: 60px; border-radius: 50%;">
//                                                  <img src="{{userprofile.profile_img.url}}" alt="" style="width: 100%; height: 100%; border-radius: 50%;" class="bg-dark">
//                                                 </div></a>
//                                               <div class="buddy-msg bg-primary ml-2 text-justify p-3">
//                                                 <p class="text-white">${value[3]}</p>
//                                                </div>
//                                         </div> 
//                                     `
//                                     $('.chat-cont').append(p)
//                                     }
//                                     else{
//                                         const p = `<div class="d-flex justify-content-center my-2 text-dark"><small style="font-size:12px;">${formatDate(value[5])}</small></div>
//                                     <div class="login-cont bg-success mb-3 p-3"><p class="text-white">${value[3]}</p></div>
//                                     `
//                                     $('.chat-cont').append(p)
//                                     }
                                   
//                                 })
//                             })
//                         },
//                     }
//                 )
//             }
//         )}, 1000
//     )
// </script>-->