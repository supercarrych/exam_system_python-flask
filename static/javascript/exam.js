// 提交试卷提示框
function submit() {
    $('#submit').click(function () {
        $('#submit_modal').modal('show')
    })
}


// 放弃考试提示框
function giveup() {
    $('#give_up').click(function () {
        $('#giveup_modal').modal('show')
    })
}

function giveupbutton() {
    $('#giveup_button').click(function () {
        window.location.href = "http://74.120.174.165:5000"
    })
}


    function getImage(img_path, containerId) {
              // 创建XMLHttpRequest对象
              var xhr = new XMLHttpRequest();

              // 发送异步请求
              xhr.open('GET', img_path, true);
              xhr.responseType = 'blob';

              xhr.onload = function() {
                if (xhr.status === 200) {
                  // 创建一个<img>元素
                  var imgElement = document.createElement('img');

                  // 从响应中获取Blob数据并将其转换为URL
                  var blob = xhr.response;
                  var imgUrl = URL.createObjectURL(blob);

                  // 设置图片的src属性
                  imgElement.src = imgUrl;
                  imgElement.alt = img_path;

                  // 将图片添加到图像容器中
                  document.getElementById(containerId).appendChild(imgElement);
                }
              };

              // 发送请求
              xhr.send();
    }



    // 获取选择的答案
function submit_question() {


            var question_input =  document.getElementById("itemid");

            var question = question_input.value;

            var id = question_input.getAttribute("itemid");

            $.ajax({
                url:'http://localhost:5000/update_question',
                type:'post',
                async: true,
                data:{
                    'id':id,
                    'question':question
                },
                success:function (res) {
                    console.log(res)
                    if (res['success'] == 1) {
                        alert('修改成功')

                    } else {
                        alert('修改失败')
                    }
                },
                error:function () {
                    alert('修改失败')
                }

            });

    }


$(document).ready(function () {
    submit()
    giveup()
    giveupbutton()
})