$('#receive').on('click', function () {
            let data = $('form').serialize();
            console.log(data);
        });


        //保存成功的提示信息
            function showResult() {
                showResultDiv(true);
                window.setTimeout("showResultDiv(false);", 3000);
            }
            function showResultDiv(flag) {
                var divResult = document.getElementById("save_result_info");
                if (flag)
                    divResult.style.display = "block";
                else
                    divResult.style.display = "none";
            }


            //显示选填的信息项
            function showOptionalInfo(imgObj) {
                var div = document.getElementById("optionalInfo");
                if (div.className == "hide") {
                    div.className = "show";
                    imgObj.src = "{% static 'images/hide.png' %}";
                }
                else {
                    div.className = "hide";
                    imgObj.src = "{% static 'images/show.png' %}";
                }
            }
