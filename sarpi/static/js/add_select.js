var choices = [];
    choices = [''];

var count = 0;

function add_hour(divName) {
    for(hour=0;hour < 24;hour++){
        for(j = 0; j < 60; j = j +10){
            if(j < 10){
                min = "0"+j;
            }else{
                min = j;
            }
            choices.push(hour+":"+min);
        }
    }

    var newDiv = document.createElement('div');
    count++;
    var selectHTML = "";
    selectHTML="<select class='input' name='hours"+count+"'>";
    for(i=0; i<choices.length; i=i+1){
        selectHTML+= "<option value='"+choices[i]+"'>"+choices[i]+"</option>";
    }
    selectHTML += "</select>";
    newDiv.innerHTML= selectHTML;
    // document.getElementById(divName).appendChild(newDiv);

    var div=document.getElementById(divName);
    div.insertBefore(newDiv, div.firstChild);

    var elem = document.getElementById("count");
    elem.value = ""+count;
}


