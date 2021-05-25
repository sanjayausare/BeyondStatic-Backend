const padCharacter = (char) => {
    let c =  String(char.charCodeAt(0))
    if(c.length===1)
    {
        c = "000" + c;
    }
    else if(c.length===2)
    {
        c = "00" + c;
    }
    else if(c.length===3)
    {
        c = "0" + c;
    }
    return c;
}

const encryptAndSend = (endpointURL, username, projectID, field1='', field2='', field3='', field4='', field5='') => {
    
    endpointURL = String(endpointURL)
    username = String(username)
    projectID = String(projectID)
    field1 = String(field1)
    field2 = String(field2)
    field3 = String(field3)
    field4 = String(field4)
    field5 = String(field5)

    let encEndpointURL = "";
    for(let i=0; i<endpointURL.length; i++)
    {
        encEndpointURL += padCharacter(endpointURL[i])
    }
    let encUsername = "";
    for(let i=0; i<username.length; i++)
    {
        encUsername += padCharacter(username[i])
    }
    let encProjectID = "";
    for(let i=0; i<projectID.length; i++)
    {
        encProjectID += padCharacter(projectID[i])
    }
    let encField1 = "";
    for(let i=0; i<field1.length; i++)
    {
        encField1 += padCharacter(field1[i])
    }
    let encField2 = "";
    for(let i=0; i<field2.length; i++)
    {
        encField2 += padCharacter(field2[i])
    }
    let encField3 = "";
    for(let i=0; i<field3.length; i++)
    {
        encField3 += padCharacter(field3[i])
    }
    let encField4 = "";
    for(let i=0; i<field4.length; i++)
    {
        encField4 += padCharacter(field4[i])
    }
    let encField5 = "";
    for(let i=0; i<field5.length; i++)
    {
        encField5 += padCharacter(field5[i])
    }

    let encURL = encEndpointURL + "zlatan" + encUsername + "zlatan" + encProjectID + "zlatan" + encField1 + "zlatan" + encField2 + "zlatan" + encField3 + "zlatan" + encField4 + "zlatan" + encField5;
    encURL = "http://127.0.0.1:8000/api/addInstance/" + encURL;

    let a = document.createElement('a');
    a.id = "sendMeMessage";
    a.href = encURL;
    document.body.appendChild(a);
    $("#sendMeMessage")[0].click();

    //you need to have jQuery installed
}


