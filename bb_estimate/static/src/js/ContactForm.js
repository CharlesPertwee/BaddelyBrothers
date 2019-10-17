var size;
function hideEnvelopes(){
    hideQuantities()
    document.getElementById("Quantity1").innerHTML = "Print Quantity 1";
    document.getElementById("Quantity2").innerHTML = "Print Quantity 2";
    document.getElementById("Quantity3").innerHTML = "Print Quantity 3";
    document.getElementById("Quantity4").innerHTML = "Print Quantity 4";
    document.getElementById("runOn").innerHTML = "Print Run on";
    document.getElementById("runOnText").innerHTML = "Provide a run on quantity for a run on price, i.e. a figure for additional envelopes more than the main run quantity";
    let ele = document.getElementsByClassName('envelope'), i;
    for (i = 0; i<ele.length;i++){
        ele[i].style.display = "none";
    }
    let elemen = document.getElementsByClassName('print'), j;
    for (j = 0; j<elemen.length;j++){
        elemen[j].style.display = "flex";
    }
    
    document.getElementById("morePara").style.display = "flex";
    document.getElementById("moreEnv").style.display = "none";
    document.getElementById("enquirySizeHeight").style.display = "none";
    document.getElementById("enquirySizeWidth").style.display = "none";
    document.getElementById("enquiryEdgeColor").style.display = "none";
}

function hidePrints(){
    hideQuantities()
    document.getElementById("Quantity1").innerHTML = "Quantity 1";
    document.getElementById("Quantity2").innerHTML = "Quantity 2";
    document.getElementById("Quantity3").innerHTML = "Quantity 3";
    document.getElementById("Quantity4").innerHTML = "Quantity 4";
    document.getElementById("runOn").innerHTML = "Run on";
    document.getElementById("runOnText").innerHTML = "Provide a run on quantity for a run on price, i.e. a figure for additional envelopes more than the main run quantity";
    let elemen = document.getElementsByClassName('print'), i;
    for (i = 0; i<elemen.length;i++){
        elemen[i].style.display = "none";
    }
    let ele = document.getElementsByClassName('envelope'), j;
    for (j = 0; j<ele.length;j++){
        ele[j].style.display = "flex";
    }
    
    document.getElementById("morePara").style.display = "flex";
    document.getElementById("moreEnv").style.display = "flex";
    document.getElementById("enquirySizeHeight").style.display = "none";
    document.getElementById("enquirySizeWidth").style.display = "none";
    document.getElementById("enquiryEdgeColor").style.display = "none";
}

function hideQuantities(){
    let extraPrints1 = document.getElementsByClassName('extra')
    for (i = 0; i<extraPrints1.length;i++){
        extraPrints1[i].style.display = "none";
    }
}

function showMoreQuantities(){
    console.log('THS IS SPARTA')
    let extraPrints = document.getElementsByClassName('extra')
        for (i = 0; i<extraPrints.length;i++){
            extraPrints[i].style.display = "flex";
        }
    
    document.getElementById("morePara").style.display = "none";
}

// function sizeEntities(){
//     alert(document.getElementById("envelopeSize").text)
// }

$(document).ready(function(){
    hidePrints()
    
    $("#envelopeSize").change(function(){
        var selectedText = $("#envelopeSize option:selected").html();
        if(selectedText == "Custom"){
            document.getElementById("enquirySizeHeight").style.display = "flex";
            document.getElementById("enquirySizeWidth").style.display = "flex";
        }else{
            document.getElementById("enquirySizeHeight").style.display = "none";
            document.getElementById("enquirySizeWidth").style.display = "none";
        }
        
    });
    
    $("#printSize").change(function(){
        var selectedText = $("#printSize option:selected").html();
        if(selectedText == "Custom"){
            document.getElementById("enquirySizeHeight").style.display = "flex";
            document.getElementById("enquirySizeWidth").style.display = "flex";
        }else{
            document.getElementById("enquirySizeHeight").style.display = "none";
            document.getElementById("enquirySizeWidth").style.display = "none";
        }
        
    });
    
    $("#enquiryPrintEdging").change(function(){
       var selectedText = $("#enquiryPrintEdging option:selected").html()
       if(selectedText == "Custom")
       {
           $("#enquiryEdgeColor").css('display','flex');
       }
       else
       {
           $("#enquiryEdgeColor").css('display','none');
       } 
    });
    
});